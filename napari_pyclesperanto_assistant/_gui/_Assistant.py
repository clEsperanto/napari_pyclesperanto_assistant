from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, Tuple
from warnings import warn

import pyclesperanto_prototype as cle
from qtpy.QtWidgets import QFileDialog, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from .._categories import CATEGORIES, Category
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
    from napari._qt.widgets.qt_viewer_dock_widget import QtViewerDockWidget
    from napari.layers import Layer
    from napari.viewer import Viewer

from napari import __version__ as napari_version
from packaging.version import parse as parse_version

npv = parse_version(napari_version)
NAP048 = (npv.major, npv.minor, npv.micro) >= (0, 4, 8)


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

        super().__init__(napari_viewer.window.qt_viewer)
        self._viewer = napari_viewer
        napari_viewer.layers.events.removed.connect(self._on_layer_removed)
        if NAP048:
            napari_viewer.layers.selection.events.changed.connect(self._on_selection)
        else:
            napari_viewer.events.active_layer.connect(self._on_active_layer_change)
        self._layers: Dict[Layer, Tuple[QtViewerDockWidget, FunctionGui]] = {}

        icon_grid = ButtonGrid(self)
        icon_grid.addItems(CATEGORIES)
        icon_grid.itemClicked.connect(self._on_item_clicked)

        export_btns = QHBoxLayout()
        # create menu
        actions = [
            ("Export Python", self.to_jython),
            ("Export Notebook", self.to_notebook),
            ("Copy to clipboard", self.to_clipboard),
        ]
        for name, cb in actions:
            btn = QPushButton(name, self)
            btn.clicked.connect(cb)
            export_btns.addWidget(btn)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(icon_grid)
        self.layout().addLayout(export_btns)

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
            self._viewer.window.remove_dock_widget(dw)
            # remove layer from internal list
            self._layers.pop(layer)

    def _on_item_clicked(self, item):
        self._activate(CATEGORIES.get(item.text()))

    def _get_active_layer(self):
        if NAP048:
            return self._viewer.layers.selection.active
        else:
            return self._viewer.active_layer

    def _activate(self, category: Category):
        # get currently active layer (before adding dock widget)
        input_layer = self._get_active_layer()
        if not input_layer:
            warn("Please select a layer first")
            return False

        # make a new widget
        gui = make_gui_for_category(category)
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
        # TODO: if the input layer changes this needs to be disconnected
        input_layer.events.data.connect(lambda x: gui())

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
            key = layer.metadata.get(OP_ID)
            if not key:
                key = "some_random_key"

            args = []
            inputs = []
            for w in mgui:
                if w.name in (VIEWER_PARAM, OP_NAME_PARAM):
                    continue
                if "napari.layers" in type(w.value).__module__:
                    op_id = w.value.metadata.get(OP_ID)
                    if op_id is None:
                        op_id = "some_random_key"
                        graph[self._id_to_name(op_id, name_dict)] = (cle.imread, ["w.value._source"], [])  # TODO
                    inputs.append(self._id_to_name(op_id, name_dict))
                else:
                    args.append(w.value)
            op = getattr(cle, getattr(mgui, OP_NAME_PARAM).value)

            # shorten args by eliminating not-used ones
            if op:
                nargs = num_positional_args(op) - 1 - len(inputs)
                args = args[:nargs]

            graph[self._id_to_name(key, name_dict)] = (op, inputs, args)

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
