from pathlib import Path

from qtpy import QtGui
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QAction, QPushButton, QFileDialog, QGridLayout

from .._gui._LayerDialog import LayerDialog
from .._scriptgenerators import JythonGenerator, PythonJupyterNotebookGenerator

class Assistant(QWidget):
    """This Gui takes a napari as parameter and infiltrates it.

    It adds some buttons for categories of _operations.
    """

    def __init__(self, napari_viewer):
        super().__init__()

        self.font = QtGui.QFont('Arial', 8)

        self.viewer = napari_viewer

        self.layout = QGridLayout()

        self._init_gui()

    def _init_gui(self):
        """Switches the GUI internally between a main menu
        where you can select categories and a sub menu where
        you can keep results or cancel processing.
        """
        # remove all buttons first
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, label_processing, map, mesh, measure, label_measurements, transform, projection

        self.add_button("Noise removal", denoise, 1, 0)
        self.add_button("Background removal", background_removal, 1, 1)
        self.add_button("Filter", filter, 1, 2)
        self.add_button("Combine", combine, 2, 0)
        self.add_button("Transform", transform, 2, 1)
        self.add_button("Projection", projection, 2, 2)

        self.add_button("Binarize", binarize, 3, 0)
        self.add_button("Label", label, 3, 1)
        self.add_button("Label processing", label_processing, 3, 2)
        self.add_button("Label measurements", label_measurements, 5, 0)
        self.add_button("Map", map, 4, 0)
        self.add_button("Mesh", mesh, 4, 1)
        self.add_button("Measure", measure, 5, 1)

        # spacer
        label = QLabel("")
        label.setFont(self.font)
        self.layout.addWidget(label, 6, 4)

        #self.layout.addStretch()

        self.setLayout(self.layout)
        #self.setMaximumWidth(300)

        # Add a menu
        action = QAction('Export Jython/Python code', self.viewer.window._qt_window)
        action.triggered.connect(self._export_jython_code)
        self.viewer.window.plugins_menu.addAction(action)

        action = QAction('Export Jython/Python code to clipboard', self.viewer.window._qt_window)
        action.triggered.connect(self._export_jython_code_to_clipboard)
        self.viewer.window.plugins_menu.addAction(action)

        action = QAction('Export Jupyter Notebook', self.viewer.window._qt_window)
        action.triggered.connect(self._export_notebook)
        self.viewer.window.plugins_menu.addAction(action)


        def _on_removed(event):
            layer = event.value
            try:
                layer.metadata['dialog']._removed()
            except AttributeError:
                pass
            except KeyError:
                pass

        self.viewer.layers.events.removed.connect(_on_removed)

    def add_button(self, title : str, handler : callable, x : int = None, y : int = None):
        # text
        btn = QPushButton('', self)
        btn.setFont(self.font)
        btn.setFixedSize(QSize(80, 80))

        # icon

        #btn.setStyleSheet("text-align:center;")

        btn.setLayout(QGridLayout())

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap()
        pixmap.load(str(Path(__file__).parent) + "/icons/" + title.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png")
        pixmap = pixmap.scaled(QSize(40, 40), Qt.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        btn.layout().addWidget(icon_label)

        text_label = QLabel(title)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setFont(self.font)
        btn.layout().addWidget(text_label)

        def trigger():
            self._activate(handler)

        # action
        btn.clicked.connect(trigger)
        if x is None or y is None:
            self.layout.addWidget(btn)
        else:
            self.layout.addWidget(btn, x, y)

    def _activate(self, magicgui):
        LayerDialog(self.viewer, magicgui)

    def _export_jython_code(self):
        generator = JythonGenerator(self.viewer.layers)
        code = generator.generate()
        self._save_code(code, default_fileending=generator.file_ending())

    def _export_jython_code_to_clipboard(self):
        generator = JythonGenerator(self.viewer.layers)
        code = generator.generate()
        import pyperclip
        pyperclip.copy(code)

    def _export_notebook(self):
        generator = PythonJupyterNotebookGenerator(self.viewer.layers)
        code = generator.generate()
        filename = self._save_code(code, default_fileending=generator.file_ending())
        if filename is not None:
            import os
            os.system('jupyter nbconvert --to notebook --inplace --execute ' + filename)
            # os.system('jupyter notebook ' + filename) # todo: this line freezes napari

    def _save_code(self, code, default_fileending = "*.*", filename = None):
        if filename is None:
            filename = QFileDialog.getSaveFileName(self, 'Save code as...', '.', default_fileending)
        if filename[0] == '':
            return None

        filename = filename[0]
        if not filename.endswith(default_fileending):
            filename = filename + default_fileending

        file = open(filename, "w+")
        file.write(code)
        file.close()

        return filename