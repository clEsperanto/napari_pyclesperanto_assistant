import warnings

import numpy as np
from magicgui.widgets import Table
from napari_plugin_engine import napari_hook_implementation
from napari.types import ImageData, LabelsData, LayerDataTuple
from napari import Viewer
from pandas import DataFrame
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QGridLayout, QPushButton, QFileDialog
import pyclesperanto_prototype as cle

def statistics_of_labeled_pixels(image: ImageData, labels: LabelsData, napari_viewer : Viewer, measure_background=False):
    """
    Adds a table widget to a given napari viewer with quantitative analysis results derived from an image-labelimage pair.
    """
    if image is not None and labels is not None:

        # quantitative analysis using clEsperanto's statistics_of_labelled_pixels
        if measure_background:
            table = cle.statistics_of_background_and_labelled_pixels(image, labels)
        else:
            table = cle.statistics_of_labelled_pixels(image, labels)

        # turn table into a widget
        dock_widget = table_to_widget(table)

        # add widget to napari
        napari_viewer.window.add_dock_widget(dock_widget, area='right')
    else:
        warnings.warn("Image and labels must be set.")

def table_to_widget(table: dict) -> QWidget:
    """
    Takes a table given as dictionary with strings as keys and numeric arrays as values and returns a QWidget which
    contains a QTableWidget with that data.
    """
    view = Table(value=table)

    copy_button = QPushButton("Copy to clipboard")
    @copy_button.clicked.connect
    def copy_trigger():
        view.to_dataframe().to_clipboard()

    save_button = QPushButton("Save as csv...")
    @save_button.clicked.connect
    def save_trigger():
        filename, _ = QFileDialog.getSaveFileName(save_button, "Save as csv...", ".", "*.csv")
        view.to_dataframe().to_csv(filename)

    widget = QWidget()
    widget.setWindowTitle("Statistics of labeled pixels")
    widget.setLayout(QGridLayout())
    widget.layout().addWidget(copy_button)
    widget.layout().addWidget(save_button)
    widget.layout().addWidget(view.native)

    return widget