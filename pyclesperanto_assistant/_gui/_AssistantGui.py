from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QAction, QPushButton


from .._gui._LayerDialog import LayerDialog
from .._scriptgenerators import PythonScriptGenerator
from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, label_processing, map, mesh, measure

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

        self._add_button("Filter (Noise removal)", self._add_denoise_clicked)
        self._add_button("Filter (Background removal)", self._add_background_removal_clicked)
        self._add_button("Filter", self._add_filter_clicked)
        self._add_button("Binarize", self._add_binarize_clicked)
        self._add_button("Combine", self._add_combine_clicked)
        self._add_button("Label", self._add_label_clicked)
        self._add_button("Label Processing", self._add_label_processing_clicked)
        self._add_button("Map", self._map_clicked)
        self._add_button("Mesh", self._mesh_clicked)
        self._add_button("Measure", self._measure_clicked)

        self.layout.addStretch()

        self.setLayout(self.layout)

        # Add a menu
        action = QAction('Export pyclesperanto code', self.viewer.window._qt_window)
        action.triggered.connect(self._export_code)
        self.viewer.window.plugins_menu.addAction(action)

        def _on_removed(event):
            layer = event.value
            try:
                layer.dialog._removed()
            except AttributeError:
                pass

        self.viewer.layers.events.removed.connect(_on_removed)

    def _add_button(self, title : str, handler : callable):
        # text
        btn = QPushButton(title, self)
        btn.setFont(QtGui.QFont('Arial', 12))

        # icon
        btn.setIcon(QtGui.QIcon(str(Path(__file__).parent) + "/icons/" + title.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"))
        btn.setIconSize(QSize(30, 30))
        btn.setStyleSheet("text-align:left;");

        # action
        btn.clicked.connect(handler)
        self.layout.addWidget(btn)

    def _add_denoise_clicked(self):
        self._activate(denoise)

    def _add_background_removal_clicked(self):
        self._activate(background_removal)

    def _add_filter_clicked(self):
        self._activate(filter)

    def _add_binarize_clicked(self):
        self._activate(binarize)

    def _add_combine_clicked(self):
        self._activate(combine)

    def _add_label_clicked(self):
        self._activate(label)

    def _add_label_processing_clicked(self):
        self._activate(label_processing)

    def _measure_clicked(self):
        self._activate(measure)

    def _map_clicked(self):
        self._activate(map)

    def _mesh_clicked(self):
        self._activate(mesh)

    def _activate(self, magicgui):
        LayerDialog(self.viewer, magicgui)

    def _export_code(self):
        print(PythonScriptGenerator(self.viewer.layers).generate())
