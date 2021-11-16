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
        from napari_skimage_regionprops import add_table
        add_table(labels_layer, napari_viewer)
    else:
        warnings.warn("Image and labels must be set.")

