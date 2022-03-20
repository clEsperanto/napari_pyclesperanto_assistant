import warnings

from napari.types import ImageData, LabelsData
from napari import Viewer
import pyclesperanto_prototype as cle
import napari

from napari_tools_menu import register_function

@register_function(menu="Measurement > Statistics of labeled pixels (clEsperanto)")
def statistics_of_labeled_pixels(image: ImageData, labels: LabelsData, napari_viewer : Viewer=None, measure_background=False):
    """
    Adds a table widget to a given napari viewer with quantitative analysis results derived from an image-labelimage pair.
    """

    if image is not None and labels is not None:

        # quantitative analysis using clEsperanto's statistics_of_labelled_pixels
        if measure_background:
            table = cle.statistics_of_background_and_labelled_pixels(image, labels)
        else:
            table = cle.statistics_of_labelled_pixels(image, labels)

        if napari_viewer is not None:
            # Store results in the properties dictionary:
            from napari_workflows._workflow import _get_layer_from_data
            labels_layer = _get_layer_from_data(napari_viewer, labels)
            labels_layer.properties = table

            # turn table into a widget
            from napari_skimage_regionprops import add_table
            add_table(labels_layer, napari_viewer)
        else:
            return table
    else:
        warnings.warn("Image and labels must be set.")

