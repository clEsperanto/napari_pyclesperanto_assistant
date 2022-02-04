from __future__ import annotations

from pathlib import Path

from typing import TYPE_CHECKING, Dict, Tuple, Callable
from warnings import warn
import napari

import pyclesperanto_prototype as cle
from qtpy.QtWidgets import QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QMenu, QLabel
from qtpy.QtGui import QCursor, QIcon

from typing import Union


from ._select_gpu import select_gpu
from .._categories import CATEGORIES, Category, filter_categories
from .._pipeline import Pipeline
from ._button_grid import ButtonGrid
from ._category_widget import (
    OP_ID,
    OP_NAME_PARAM,
    VIEWER_PARAM,
    make_gui_for_category,
    num_positional_args
)

if TYPE_CHECKING:
    from magicgui.widgets import FunctionGui
    from napari.layers import Layer
    from napari.viewer import Viewer

from napari import __version__ as napari_version
from packaging.version import parse as parse_version
from napari_tools_menu import register_dock_widget

npv = parse_version(napari_version)
NAP048 = (npv.major, npv.minor, npv.micro) >= (0, 4, 8)

@register_dock_widget(menu="Utilities > Assistant (clEsperanto)")
class Assistant(QWidget):
    """The main cle Assistant widget.

    The widget holds buttons with icons to create widgets for the various
    cel operation categories.  It tracks which layers are connected to which
    widgets, and can export the state of the task graph to a dask graph
    or to jython code.

    Parameters
    ----------
    napari_viewer : Viewer
        This viewer instance will be provided by napari when it gets added
        as a plugin dock widget.
    """

    def __init__(self, napari_viewer: Viewer):

        super().__init__()
        self._viewer = napari_viewer
        napari_viewer.layers.events.removed.connect(self._on_layer_removed)
        napari_viewer.layers.selection.events.changed.connect(self._on_selection)
        self._layers = {}

        # visualize intermediate results human-readable from top-left to bottom-right
        self._viewer.grid.stride = -1

        CATEGORIES["Measure"] = self._measure
        CATEGORIES["Generate code..."] = self._code_menu

        # build GUI
        icon_grid = ButtonGrid(self)
        icon_grid.addItems(CATEGORIES)
        icon_grid.itemClicked.connect(self._on_item_clicked)

        self.seach_field = QLineEdit("")
        def text_changed(*args, **kwargs):
            search_string = self.seach_field.text().lower()
            icon_grid.clear()
            icon_grid.addItems(filter_categories(search_string))

        self.seach_field.textChanged.connect(text_changed)


        # create menu
        self.actions = [
            ("Export Python script to file", self.to_jython),
            ("Export Jupyter Notebook", self.to_notebook),
            ("Copy to clipboard", self.to_clipboard),
            ("Export workflow to file", self.to_file)
        ]

        # add Send to script editor menu in case it's installed
        try:
            import napari_script_editor
            self.actions.append(("Send to Script Editor", self.to_script_editor))
        except ImportError:
            pass

        self.setLayout(QVBoxLayout())
        search_and_help = QWidget()
        search_and_help.setLayout(QHBoxLayout())
        from ._button_grid import _get_icon
        help = QLabel("?")
        help.setToolTip(
            '<html>'
            'Use the search field on the left to enter a term describing the function you would like to apply to your image.\n'
            'Searching will limit the number of shown categories and listed operations.\n'
            '<br><br>The icons in the buttons below denote the processed image types:\n'
            '<br><img src="' + _get_icon("intensity_image") + '" width="24" heigth="24"> In <b>intensity images</b> the pixel value represents a measurement, e.g. of collected light during acquisition in a microscope.\n'
            '<br><img src="' + _get_icon("binary_image") + '" width="24" heigth="24"> In <b>binary images</b> pixels with value 0 mean there is no object present. All other pixels (typically value 1) represent any object.\n'
            '<br><img src="' + _get_icon("label_image") + '" width="24" heigth="24"> In <b>label images</b> the integer pixel intensity corresponds to the object identity. E.g. all pixels of object 2 have value 2.\n'
            '<br><img src="' + _get_icon("parametric_image") + '" width="24" heigth="24"> In <b>parametric images</b> the pixel value represents an object measurement. All pixels of an object can for example contain the same value, e.g. the objects circularity or area.\n'
            '<br><img src="' + _get_icon("mesh_image") + '" width="24" heigth="24"> In <b>mesh images</b> we can visualize connectivity between objects and distances as intensity along lines.\n'
            '<br><img src="' + _get_icon("any_image") + '" width="24" heigth="24"> This icon means one can use <b>any kind of image</b> for this operation.'
            '</html>'
        )
        help.setMaximumWidth(20)
        search_and_help.layout().addWidget(self.seach_field)
        search_and_help.layout().addWidget(help)

        self.layout().addWidget(search_and_help)
        self.layout().addWidget(icon_grid)

        self.layout().setContentsMargins(5, 5, 5, 5)
        self.setMinimumWidth(345)

        select_gpu()

    def _measure(self):
        from .._statistics_of_labeled_pixels import statistics_of_labeled_pixels
        self._viewer.window.add_function_widget(statistics_of_labeled_pixels)

    def _code_menu(self):
        menu = QMenu(self)

        for name, cb in self.actions:
            submenu = menu.addAction(name)
            submenu.triggered.connect(cb)

        menu.move(QCursor.pos())
        menu.show()

    def _on_selection(self, event):
        for layer, (dw, gui) in self._layers.items():
            if layer in self._viewer.layers.selection:
                dw.show()
            else:
                dw.hide()

    def _on_active_layer_change(self, event):
        for layer, (dw, gui) in self._layers.items():
            dw.show() if event.value is layer else dw.hide()

    def _on_layer_removed(self, event):
        layer = event.value
        if layer in self._layers:
            dw = self._layers[layer][0]
            try:
                self._viewer.window.remove_dock_widget(dw)
            except KeyError:
                pass
            # remove layer from internal list
            self._layers.pop(layer)

    def _on_item_clicked(self, item):
        self._activate(CATEGORIES.get(item.text()))

    def _get_active_layer(self):
        return self._viewer.layers.selection.active

    def _activate(self, category = Union[Category, Callable]):
        if callable(category):
            category()
            return

        # get currently active layer (before adding dock widget)
        input_layer = self._get_active_layer()
        if not input_layer:
            warn("Please select a layer first")
            return False

        # make a new widget
        gui = make_gui_for_category(category, self.seach_field.text(), self._viewer)
        # prevent auto-call when adding to the viewer, to avoid double calls
        # do this here rather than widget creation for the sake of
        # non-Assistant-based widgets.
        gui._auto_call = False
        # add gui to the viewer
        dw = self._viewer.window.add_dock_widget(gui, area="right", name=category.name)
        # make sure the originally active layer is the input
        try:
            gui.input0.value = input_layer
        except ValueError:
            pass # this happens if input0 should be labels but we provide an image
        # call the function widget &
        # track the association between the layer and the gui that generated it
        self._layers[gui()] = (dw, gui)
        # turn on auto_call, and make sure that if the input changes we update
        gui._auto_call = True
        self._connect_to_all_layers()

    def _refesh_data(self, event):
        self._refresh(event.source)

    def _refresh(self, changed_layer):
        """Goes through all layers and refreshs those which have changed_layer as input

        Parameters
        ----------
        changed_layer
        """
        for layer, (dw, mgui) in self._layers.items():
            for w in mgui:
                if w.value == changed_layer:
                    mgui()

    def _connect_to_all_layers(self):
        """Attach an event listener to all layers that are currently open in napari
        """
        for layer in self._viewer.layers:
            layer.events.data.disconnect(self._refesh_data)
            layer.events.data.connect(self._refesh_data)

    def load_sample_data(self, fname="Lund_000500_resampled-cropped.tif"):
        data_dir = Path(__file__).parent.parent / "data"
        self._viewer.open(str(data_dir / fname))

    def _id_to_name(self, id, dict):
        if id not in dict.keys():
            new_name = "image" + str(len(dict.keys()))
            dict[id] = new_name
        return dict[id]

    def to_dask(self):
        graph = {}
        name_dict = {}
        for layer, (dw, mgui) in self._layers.items():
            key = None
            if isinstance(layer.metadata, dict):
                key = layer.metadata.get(OP_ID)

            if key is None:
                key = "some_random_key"

            args = []
            inputs = []
            for w in mgui:
                if w.name in (VIEWER_PARAM, OP_NAME_PARAM):
                    continue
                if "napari.layers" in type(w.value).__module__:
                    op_id = None
                    if isinstance(w.value.metadata, dict):
                        op_id = w.value.metadata.get(OP_ID)
                    if op_id is None:
                        op_id = "some_random_key"
                        source = str(w.value.source.path).replace("\\", "/") if w.value.source is not None else "file"
                        graph[self._id_to_name(op_id, name_dict)] = (cle.imread, ["'" + source + "'"], [], False, layer.contrast_limits[0], layer.contrast_limits[1])  # TODO
                    inputs.append(self._id_to_name(op_id, name_dict))
                else:
                    args.append(w.value)
            from .._categories import find_function
            op = find_function(getattr(mgui, OP_NAME_PARAM).value)
            #getattr(cle, getattr(mgui, OP_NAME_PARAM).value)

            # shorten args by eliminating not-used ones
            if op:
                nargs = num_positional_args(op) - 1 - len(inputs)
                args = args[:nargs]

            is_labels = isinstance(layer, napari.layers.Labels)
            graph[self._id_to_name(key, name_dict)] = (op, inputs, args, is_labels, layer.contrast_limits[0], layer.contrast_limits[1])

        return graph

    def to_jython(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(self, "Save code as...", ".", "*.py")
        return Pipeline.from_assistant(self).to_jython(filename)

    def to_notebook(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(self, "Save code as notebook...", ".", "*.ipynb")
        return Pipeline.from_assistant(self).to_notebook(filename)

    def to_clipboard(self):
        import pyperclip

        pyperclip.copy(Pipeline.from_assistant(self).to_jython())

    def to_script_editor(self):
        import napari_script_editor
        editor = napari_script_editor.ScriptEditor.get_script_editor_from_viewer(self._viewer)
        editor.set_code(Pipeline.from_assistant(self).to_napari_python())

    def to_file(self, filename=None):
        from napari_workflows import WorkflowManager, _io_yaml_v1

        if not filename:
            filename, _ = QFileDialog.getSaveFileName(self, "Export workflow ...", ".", "*.yaml")

        # get the workflow, should one be installed
        workflow_manager = WorkflowManager.install(self._viewer)
        _io_yaml_v1.save_workflow(filename, workflow_manager.workflow)
