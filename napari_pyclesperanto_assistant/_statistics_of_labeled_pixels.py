import warnings

import numpy as np
from magicgui.widgets import Table
from napari_plugin_engine import napari_hook_implementation
from napari.types import ImageData, LabelsData, LayerDataTuple
from napari import Viewer
from pandas import DataFrame
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QGridLayout, QPushButton, QFileDialog
import pyclesperanto_prototype as cle
import napari

from napari_tools_menu import register_function

@register_function(menu="Measurement > Statistics of labeled pixels (clEsperanto)")
def statistics_of_labeled_pixels(image: ImageData, labels_layer: napari.layers.Labels, napari_viewer : Viewer, measure_background=False):
    """
    Adds a table widget to a given napari viewer with quantitative analysis results derived from an image-labelimage pair.
    """
    labels = labels_layer.data

    if image is not None and labels is not None:

        # quantitative analysis using clEsperanto's statistics_of_labelled_pixels
        if measure_background:
            table = cle.statistics_of_background_and_labelled_pixels(image, labels)
        else:
            table = cle.statistics_of_labelled_pixels(image, labels)

        # Store results in the properties dictionary:
        labels_layer.properties = table

        # turn table into a widget
        dock_widget = table_to_widget(table, labels_layer)

        # add widget to napari
        napari_viewer.window.add_dock_widget(dock_widget, area='right')
    else:
        warnings.warn("Image and labels must be set.")

# taken from https://github.com/haesleinhuepf/napari-skimage-regionprops/blob/master/napari_skimage_regionprops/_regionprops.py#L90
def table_to_widget(table: dict, labels_layer: napari.layers.Labels) -> QWidget:
    """
    Takes a table given as dictionary with strings as keys and numeric arrays as values and returns a QWidget which
    contains a QTableWidget with that data.
    """
    # Using a custom widget because this one freezes napari:
    # view = Table(value=table)
    view = QTableWidget(len(next(iter(table.values()))), len(table))
    for i, column in enumerate(table.keys()):
        view.setItem(0, i, QTableWidgetItem(column))
        for j, value in enumerate(table.get(column)):
            view.setItem(j + 1, i, QTableWidgetItem(str(value)))

    if labels_layer is not None:

        @view.clicked.connect
        def clicked_table():
            row = view.currentRow()
            label = table["label"][row]
            labels_layer.selected_label = label

        def after_labels_clicked():
            row = view.currentRow()
            label = table["label"][row]
            if label != labels_layer.selected_label:
                for r, l in enumerate(table["label"]):
                    if l ==  labels_layer.selected_label:
                        view.setCurrentCell(r, view.currentColumn())
                        break

        @labels_layer.mouse_drag_callbacks.append
        def clicked_labels(event, event1):
            # We need to run this lagter as the labels_layer.selected_label isn't changed yet.
            QTimer.singleShot(200, after_labels_clicked)


    copy_button = QPushButton("Copy to clipboard")

    @copy_button.clicked.connect
    def copy_trigger():
        DataFrame(table).to_clipboard()

    save_button = QPushButton("Save as csv...")

    @save_button.clicked.connect
    def save_trigger():
        filename, _ = QFileDialog.getSaveFileName(save_button, "Save as csv...", ".", "*.csv")
        DataFrame(table).to_csv(filename)

    widget = QWidget()
    widget.setWindowTitle("region properties")
    widget.setLayout(QGridLayout())
    widget.layout().addWidget(copy_button)
    widget.layout().addWidget(save_button)
    widget.layout().addWidget(view)

    return widget