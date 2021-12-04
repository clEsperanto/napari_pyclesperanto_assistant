import pyclesperanto_prototype as cle
import napari
from napari.layers import Image, Labels, Layer
from napari.types import ImageData, LabelsData
from napari_tools_menu import register_function, register_action
from napari_time_slicer import time_slicer

@register_function(menu="Segmentation / labeling > Connected component labeling (clesperanto)")
@time_slicer
def label(binary_image: napari.types.LabelsData, viewer: napari.Viewer = None) -> napari.types.LabelsData:
    result = cle.connected_components_labeling_box(binary_image)
    return result


@register_function(menu="Segmentation / labeling > Voronoi-Otsu-labeling (clesperanto)")
@time_slicer
def voronoi_otsu_labeling(image:ImageData, spot_sigma: float = 2, outline_sigma: float = 2, viewer: napari.Viewer = None) -> LabelsData:
    return cle.voronoi_otsu_labeling(image, spot_sigma=spot_sigma, outline_sigma=outline_sigma)

