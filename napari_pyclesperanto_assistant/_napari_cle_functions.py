import pyclesperanto_prototype as cle
import napari
from napari.types import ImageData, LabelsData
from napari_tools_menu import register_function
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


@register_function(menu="Segmentation post-processing > Smooth labels (clesperanto)", radius={"widget_type": "FloatSlider", "min": 0, "max":10}, auto_call=True)
@time_slicer
def smooth_labels(labels:LabelsData, radius: float = 1) -> LabelsData:
    return cle.smooth_labels(labels, radius=radius)


@register_function(menu="Segmentation post-processing > Merge labels with intensity along borders within range (clesperanto)",
                   minimum_intensity={"min": 0, "max":100000},
                   maximum_intensity={"min": 0, "max":100000},
                   auto_call=True)
@time_slicer
def merge_labels_with_border_intensity_within_range(image:ImageData, labels:LabelsData, minimum_intensity: float = 0, maximum_intensity: float = 1000) -> LabelsData:
    return cle.merge_labels_with_border_intensity_within_range(image,
                                                               labels,
                                                               minimum_intensity=minimum_intensity,
                                                               maximum_intensity=maximum_intensity
                                                               )
