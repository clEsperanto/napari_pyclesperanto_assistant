from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QAction, QPushButton, QFileDialog

from .._gui._LayerDialog import LayerDialog
from .._scriptgenerators import PythonGenerator, JythonGenerator, PythonJupyterNotebookGenerator

class AssistantGUI(QWidget):
    """This Gui takes a napari as parameter and infiltrates it.

    It adds some buttons for categories of _operations.
    """

    def __init__(self, viewer):
        super().__init__()

        self.viewer = viewer

        self.layout = QVBoxLayout()

        self._init_gui()

    def _init_gui(self):
        """Switches the GUI internally between a main menu
        where you can select categories and a sub menu where
        you can keep results or cancel processing.
        """
        # remove all buttons first
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        label = QLabel("Add layer")
        label.setFont(QtGui.QFont('Arial', 12))
        label.setFixedSize(QSize(300, 30))
        self.layout.addWidget(label)

        from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, label_processing, map, mesh, measure

        self.add_button("Filter (Noise removal)", denoise)
        self.add_button("Filter (Background removal)", background_removal)
        self.add_button("Filter", filter)
        self.add_button("Binarize", binarize)
        self.add_button("Combine", combine)
        self.add_button("Label", label)
        self.add_button("Label Processing", label_processing)
        self.add_button("Map", map)
        self.add_button("Mesh", mesh)
        self.add_button("Measure", measure)

        self.layout.addStretch()

        self.setLayout(self.layout)
        self.setMaximumWidth(300)

        # Add a menu
        #action = QAction('Export Python code', self.viewer.window._qt_window)
        #action.triggered.connect(self._export_python_code)
        #self.viewer.window.plugins_menu.addAction(action)

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

    def add_button(self, title : str, handler : callable):
        # text
        btn = QPushButton(title, self)
        btn.setFont(QtGui.QFont('Arial', 12))

        # icon
        btn.setIcon(QtGui.QIcon(str(Path(__file__).parent) + "/icons/" + title.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"))
        btn.setIconSize(QSize(20, 20))
        btn.setStyleSheet("text-align:left;")

        def trigger():
            self._activate(handler)

        # action
        btn.clicked.connect(trigger)
        self.layout.addWidget(btn)

    def _activate(self, magicgui):
        LayerDialog(self.viewer, magicgui)

    def _export_python_code(self):
        generator = PythonGenerator(self.viewer.layers)
        code = generator.generate()
        self._save_code(code, default_fileending=generator.file_ending())

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