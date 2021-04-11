from pathlib import Path
from PyQt5.QtWidgets import QMenu

from qtpy.QtWidgets import QAction, QFileDialog, QVBoxLayout, QWidget

from .._gui._LayerDialog import LayerDialog
from .._scriptgenerators import JythonGenerator, PythonJupyterNotebookGenerator
from ._button_grid import ButtonGrid
from .._operations import _operations


class Assistant(QWidget):
    """This Gui takes a napari as parameter and infiltrates it.

    It adds some buttons for categories of _operations.
    """

    def __init__(self, napari_viewer):
        super().__init__(napari_viewer.window.qt_viewer)
        self.viewer = napari_viewer
        self.viewer.layers.events.removed.connect(self._on_layer_removed)

        self._grid = ButtonGrid(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._grid)
        self._grid.addItems(_operations.OPERATION_NAMES)
        self._grid.itemClicked.connect(self._on_item_clicked)

        # create menu
        self._cle_menu = QMenu("clEsperanto", self.viewer.window._qt_window)
        self.viewer.window.plugins_menu.addMenu(self._cle_menu)
        actions = [
            ("Export Jython/Python code", self._export_jython_code),
            ("Export Jython/Python code to clipboard", self._export_jython_code_to_clipboard),
            ("Export Jupyter Notebook", self._export_notebook),
        ]
        for name, cb in actions:
            action = QAction(name, self)
            action.triggered.connect(cb)
            self._cle_menu.addAction(action)

    def _on_layer_removed(self, event):
        layer = event.value
        try:
            layer.metadata["dialog"]._removed()
        except AttributeError:
            pass
        except KeyError:
            pass

    def _on_item_clicked(self, item):
        self._activate(_operations.OPERATION_NAMES.get(item.text()))

    def _activate(self, op_name: str):
        from magicgui import magicgui

        _k = {"call_button": "Measure"} if op_name == "measure" else {"auto_call": True}
        widget = magicgui(getattr(_operations, op_name), **_k)
        LayerDialog(self.viewer, widget)
        return widget

    def load_sample_data(self, fname="Lund_000500_resampled-cropped.tif"):
        data_dir = Path(__file__).parent.parent / "data"
        self.viewer.open(str(data_dir / fname))

    # TODO: move code generation to another module

    def _export_jython_code(self):
        generator = JythonGenerator(self.viewer.layers)
        code = generator.generate()
        self._save_code(code, default_fileending=generator.file_ending())

    def _export_jython_code_to_clipboard(self):
        generator = JythonGenerator(self.viewer.layers)
        code = generator.generate()
        import pyperclip

        pyperclip.copy(code)

    def _export_notebook(self, filename=None):
        generator = PythonJupyterNotebookGenerator(self.viewer.layers)
        code = generator.generate()
        if filename is None:
            filename = self._save_code(code, default_fileending=generator.file_ending())
        if filename is not None:
            import os

            # NOTE: probably better to use subprocess.run here?
            os.system("jupyter nbconvert --to notebook --inplace --execute " + filename)
            # os.system('jupyter notebook ' + filename) # todo: this line freezes napari

    def _save_code(self, code, default_fileending="*.*", filename=None):
        if filename is None:
            filename = QFileDialog.getSaveFileName(
                self, "Save code as...", ".", default_fileending
            )
        if filename[0] == "":
            return None

        filename = filename[0]
        if not filename.endswith(default_fileending):
            filename = filename + default_fileending

        with open(filename, "w+") as file:
            file.write(code)
        return filename
