from __future__ import annotations
import pyclesperanto_prototype as cle

from pathlib import Path
from typing import Dict, TYPE_CHECKING, Tuple
from warnings import warn

from qtpy.QtWidgets import QAction, QFileDialog, QMenu, QVBoxLayout, QWidget

from .._categories import CATEGORIES, Category
from ._category_widget import make_gui_for_category, OP_ID, VIEWER_PARAM, OP_NAME_PARAM

from ._button_grid import ButtonGrid

if TYPE_CHECKING:
    from napari.layers import Layer
    from napari.viewer import Viewer
    from napari._qt.widgets.qt_viewer_dock_widget import QtViewerDockWidget
    from magicgui.widgets import FunctionGui


class Assistant(QWidget):
    """This Gui takes a napari as parameter and infiltrates it.

    It adds some buttons for categories of _operations.
    """

    def __init__(self, napari_viewer: Viewer):
        super().__init__(napari_viewer.window.qt_viewer)
        self.viewer = napari_viewer
        napari_viewer.layers.events.removed.connect(self._on_layer_removed)
        napari_viewer.events.active_layer.connect(self._on_active_layer_change)
        self._layers: Dict[Layer, Tuple[QtViewerDockWidget, FunctionGui]] = {}

        self._grid = ButtonGrid(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._grid)
        self._grid.addItems(CATEGORIES)
        self._grid.itemClicked.connect(self._on_item_clicked)

        # # create menu
        # self._cle_menu = QMenu("clEsperanto", self.viewer.window._qt_window)
        # self.viewer.window.plugins_menu.addMenu(self._cle_menu)
        # actions = [
        #     ("Export Jython/Python code", self._export_jython_code),
        #     (
        #         "Export Jython/Python code to clipboard",
        #         self._export_jython_code_to_clipboard,
        #     ),
        #     ("Export Jupyter Notebook", self._export_notebook),
        # ]
        # for name, cb in actions:
        #     action = QAction(name, self)
        #     action.triggered.connect(cb)
        #     self._cle_menu.addAction(action)

    def _on_active_layer_change(self, event):
        for layer, (dw, gui) in self._layers.items():
            dw.show() if event.value is layer else dw.hide()

    def _on_layer_removed(self, event):
        layer = event.value
        if layer in self._layers:
            dw = self._layers[layer][0]
            self.viewer.window.remove_dock_widget(dw)
            # remove layer from internal list
            self._layers.pop(layer)

    def _on_item_clicked(self, item):
        self._activate(CATEGORIES.get(item.text()))

    def _activate(self, category: Category):
        if not self.viewer.active_layer:
            warn("Please select a layer first")
            return

        # make a new widget
        gui = make_gui_for_category(category)
        # get currently active layer (before adding dock widget)
        input_layer = self.viewer.active_layer
        # add gui to the viewer
        dw = self.viewer.window.add_dock_widget(gui, area="right", name=category.name)
        # make sure the originally active layer is the input
        gui.input0.value = input_layer
        # call the function widget &
        # track the association between the layer and the gui that generated it
        self._layers[gui()] = (dw, gui)
        # turn on auto_call, and make sure that if the input changes we update
        gui._auto_call = True
        # TODO: if the input layer changes this needs to be disconnected
        input_layer.events.data.connect(lambda x: gui())

    def load_sample_data(self, fname="Lund_000500_resampled-cropped.tif"):
        data_dir = Path(__file__).parent.parent / "data"
        self.viewer.open(str(data_dir / fname))

    def to_dask(self):
        graph = {}
        for layer, (dw, mgui) in self._layers.items():
            key = id(mgui)
            args = []
            for w in mgui:
                if w.name in (VIEWER_PARAM, OP_NAME_PARAM):
                    continue
                if "napari.layers" in type(w.value).__module__:
                    op_id = w.value.metadata.get(OP_ID)
                    if op_id is None:
                        op_id = "some_random_key"
                        graph[op_id] = (cle.imread, "w.value._source")  # TODO
                    args.append(op_id)
                else:
                    args.append(w.value)
            op = getattr(cle, getattr(mgui, OP_NAME_PARAM).value)
            graph[key] = (op, *args)
        return graph

    def to_jython(self):
        from .._pipeline import Pipeline

        return str(Pipeline.from_assistant(self))
