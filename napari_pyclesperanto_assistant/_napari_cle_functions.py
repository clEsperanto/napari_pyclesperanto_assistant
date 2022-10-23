import pyclesperanto_prototype as cle
from napari_tools_menu import register_function
from napari_time_slicer import time_slicer

def _package_ncle(func):
    func.__module__ = "napari_pyclesperanto_assistant"
    if hasattr(cle, func.__name__):
        func.__doc__ = getattr(cle, func.__name__).__doc__
    return func

@register_function(menu="Segmentation / labeling > Connected component labeling (clesperanto)")
@time_slicer
@_package_ncle
def label(binary_image: "napari.types.LabelsData") -> "napari.types.LabelsData":
    """Connected component labeling using box-neighborhood (8-connected in 2D, 26-connected in 3D)"""
    result = cle.connected_components_labeling_box(binary_image)
    return result


@register_function(menu="Segmentation / labeling > Voronoi-Otsu-labeling (clesperanto)")
@time_slicer
@_package_ncle
def voronoi_otsu_labeling(image:"napari.types.ImageData", spot_sigma: float = 2, outline_sigma: float = 2) -> "napari.types.LabelsData":
    return cle.voronoi_otsu_labeling(image, spot_sigma=spot_sigma, outline_sigma=outline_sigma)


@register_function(menu="Segmentation post-processing > Smooth labels (clesperanto)", radius={"widget_type": "FloatSlider", "min": 0, "max":10}, auto_call=True)
@time_slicer
@_package_ncle
def smooth_labels(labels:"napari.types.LabelsData", radius: float = 1) -> "napari.types.LabelsData":
    return cle.smooth_labels(labels, radius=radius)


@register_function(menu="Segmentation post-processing > Merge touching labels with intensity along borders within range (clesperanto)",
                   minimum_intensity={"min": 0, "max":100000},
                   maximum_intensity={"min": 0, "max":100000},
                   auto_call=True)
@time_slicer
@_package_ncle
def merge_labels_with_border_intensity_within_range(image:"napari.types.ImageData", labels:"napari.types.LabelsData", minimum_intensity: float = 0, maximum_intensity: float = 1000) -> "napari.types.LabelsData":
    return cle.merge_labels_with_border_intensity_within_range(image,
                                                               labels,
                                                               minimum_intensity=minimum_intensity,
                                                               maximum_intensity=maximum_intensity
                                                               )


@register_function(menu="Segmentation post-processing > Merge touching labels (clesperanto)")
@time_slicer
@_package_ncle
def merge_touching_labels(labels:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.merge_touching_labels(labels)
merge_touching_labels.__doc__ = cle.merge_touching_labels.__doc__


@register_function(menu="Segmentation post-processing > Dilate Labels (clesperanto)")
@time_slicer
@_package_ncle
def dilate_labels(labels:"napari.types.LabelsData", radius: int = 1) -> "napari.types.LabelsData":
    return cle.dilate_labels(labels, radius=radius)


@register_function(menu="Segmentation post-processing > Erode Labels (clesperanto)")
@time_slicer
@_package_ncle
def erode_labels(labels:"napari.types.LabelsData", radius: int = 1) -> "napari.types.LabelsData":
    return cle.erode_labels(labels, radius=radius)


@register_function(menu="Segmentation post-processing > Opening Labels (clesperanto)")
@time_slicer
@_package_ncle
def opening_labels(labels:"napari.types.LabelsData", radius: int = 1) -> "napari.types.LabelsData":
    return cle.opening_labels(labels, radius=radius)


@register_function(menu="Segmentation post-processing > Closing Labels (clesperanto)")
@time_slicer
@_package_ncle
def closing_labels(labels:"napari.types.LabelsData", radius: int = 1) -> "napari.types.LabelsData":
    return cle.closing_labels(labels, radius=radius)



