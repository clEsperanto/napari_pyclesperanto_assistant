import pyclesperanto as cle
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
    result = cle.connected_components_labeling(binary_image)
    return result


@register_function(menu="Segmentation / labeling > Voronoi-Otsu-labeling (clesperanto)")
@time_slicer
@_package_ncle
def voronoi_otsu_labeling(image:"napari.types.ImageData", spot_sigma: float = 2, outline_sigma: float = 2) -> "napari.types.LabelsData":
    return cle.voronoi_otsu_labeling(image, spot_sigma=spot_sigma, outline_sigma=outline_sigma)


@register_function(menu="Segmentation / labeling > Eroded-Otsu-labeling (clesperanto)")
@time_slicer
@_package_ncle
def eroded_otsu_labeling(image:"napari.types.ImageData", number_of_erosions: int = 2, outline_sigma: float = 2) -> "napari.types.LabelsData":
    return cle.eroded_otsu_labeling(image, number_of_erosions=number_of_erosions, outline_sigma=outline_sigma)


@register_function(menu="Segmentation / labeling > Gauss-Otsu-labeling (clesperanto)")
@time_slicer
@_package_ncle
def gauss_otsu_labeling(image:"napari.types.ImageData", outline_sigma: float = 2) -> "napari.types.LabelsData":
    return cle.gauss_otsu_labeling(image, outline_sigma=outline_sigma)


@register_function(menu="Filtering / background removal > Top-hat (box, clesperanto)")
@time_slicer
@_package_ncle
def top_hat_box(image:"napari.types.ImageData", radius_x: int = 10, radius_y: int = 10, radius_z: int = 0) -> "napari.types.ImageData":
    return cle.top_hat(image, radius_x=radius_x, radius_y=radius_y, radius_z=radius_z)


@register_function(menu="Filtering / noise removal > Mean (box, clesperanto)")
@time_slicer
@_package_ncle
def mean_box(image:"napari.types.ImageData", radius_x: int = 10, radius_y: int = 10, radius_z: int = 0) -> "napari.types.ImageData":
    return cle.mean(image, radius_x=radius_x, radius_y=radius_y, radius_z=radius_z)


@register_function(menu="Filtering > Difference of Gaussian (clesperanto)")
@time_slicer
@_package_ncle
def difference_of_gaussian(image:"napari.types.ImageData",
                           sigma1_x: float = 1, sigma1_y: float = 1, sigma1_z: float = 0,
                           sigma2_x: float = 10, sigma2_y: float = 10, sigma2_z: float = 0,
                           ) -> "napari.types.ImageData":
    return cle.difference_of_gaussian(image,
                                      sigma1_x=sigma1_x, sigma1_y=sigma1_y, sigma1_z=sigma1_z,
                                      sigma2_x=sigma2_x, sigma2_y=sigma2_y, sigma2_z=sigma2_z
                                      )


@register_function(menu="Filtering > Laplacian of Gaussian (clesperanto)")
@time_slicer
def laplacian_of_gaussian(image:"napari.types.ImageData",
                           sigma_x: float = 1, sigma_y: float = 1, sigma_z: float = 0,
                           ) -> "napari.types.ImageData":
    """Applies a Laplace-box filter to a Gaussian-blurred image of the original.
    That might be useful for edge detection"""
    return cle.laplace(
                           cle.gaussian_blur(image,
                                      sigma_x=sigma_x, sigma_y=sigma_y, sigma_z=sigma_z,
                           )
    )


@register_function(menu="Filtering / noise removal > Gaussian (clesperanto)")
@time_slicer
def gaussian_blur(image:"napari.types.ImageData",
                           sigma_x: float = 1, sigma_y: float = 1, sigma_z: float = 0,
                           ) -> "napari.types.ImageData":
    return cle.gaussian_blur(image,
                      sigma_x=sigma_x, sigma_y=sigma_y, sigma_z=sigma_z,
           )


@register_function(menu="Filtering / background removal > Subtract Gaussian background (clesperanto)")
@time_slicer
@_package_ncle
def subtract_gaussian_background(image:"napari.types.ImageData", sigma_x: float = 1, sigma_y: float = 1, sigma_z: float = 0) -> "napari.types.ImageData":
    return cle.subtract_gaussian_background(image, sigma_x=sigma_x, sigma_y=sigma_y, sigma_z=sigma_z)


@register_function(menu="Filtering / background removal > Divide by Gaussian background (clesperanto)")
@time_slicer
@_package_ncle
def divide_by_gaussian_background(image:"napari.types.ImageData", sigma_x: float = 1, sigma_y: float = 1, sigma_z: float = 0) -> "napari.types.ImageData":
    return cle.divide_by_gaussian_background(image, sigma_x=sigma_x, sigma_y=sigma_y, sigma_z=sigma_z)


@register_function(menu="Filtering > Small Hessian eigenvalue (clesperanto)")
@time_slicer
@_package_ncle
def small_hessian_eigenvalue(image:"napari.types.ImageData") -> "napari.types.ImageData":
    return cle.small_hessian_eigenvalue(image)


@register_function(menu="Filtering > Large Hessian eigenvalue (clesperanto)")
@time_slicer
@_package_ncle
def large_hessian_eigenvalue(image:"napari.types.ImageData") -> "napari.types.ImageData":
    return cle.large_hessian_eigenvalue(image)


@register_function(menu="Filtering / edge enhancement > Standard deviation (box, clesperanto)")
@time_slicer
@_package_ncle
def standard_deviation_box(image:"napari.types.ImageData", radius_x: int = 10, radius_y: int = 10, radius_z: int = 0) -> "napari.types.ImageData":
    return cle.standard_deviation(image, radius_x=radius_x, radius_y=radius_y, radius_z=radius_z)


@register_function(menu="Filtering / edge enhancement > Variance (box, clesperanto)")
@time_slicer
@_package_ncle
def variance_box(image:"napari.types.ImageData", radius_x: int = 10, radius_y: int = 10, radius_z: int = 0) -> "napari.types.ImageData":
    return cle.variance(image, radius_x=radius_x, radius_y=radius_y, radius_z=radius_z)


@register_function(menu="Segmentation post-processing > Exclude large labels (clesperanto)")
@time_slicer
@_package_ncle
def exclude_large_labels(labels:"napari.types.LabelsData", minimum_size: float = 1) -> "napari.types.LabelsData":
    return cle.exclude_large_labels(labels, minimum_size=minimum_size)


@register_function(menu="Segmentation post-processing > Exclude small labels (clesperanto)")
@time_slicer
@_package_ncle
def exclude_small_labels(labels:"napari.types.LabelsData", maximum_size: float = 1) -> "napari.types.LabelsData":
    return cle.exclude_small_labels(labels, maximum_size=maximum_size)


@register_function(menu="Segmentation post-processing > Exclude labels with map values out of range (clesperanto)")
@time_slicer
@_package_ncle
def exclude_labels_with_map_values_out_of_range(values_map:"napari.types.ImageData", labels:"napari.types.LabelsData", minimum_value_range: float = 0, maximum_value_range: float=100) -> "napari.types.LabelsData":
    return cle.exclude_labels_with_map_values_out_of_range(values_map, labels, minimum_value_range=minimum_value_range, maximum_value_range=maximum_value_range)


@register_function(menu="Segmentation post-processing > Exclude labels with map values within range (clesperanto)")
@time_slicer
@_package_ncle
def exclude_labels_with_map_values_within_range(values_map:"napari.types.ImageData", labels:"napari.types.LabelsData", minimum_value_range: float = 0, maximum_value_range: float=100) -> "napari.types.LabelsData":
    return cle.exclude_labels_with_map_values_within_range(values_map, labels, minimum_value_range=minimum_value_range, maximum_value_range=maximum_value_range)

@register_function(menu="Segmentation post-processing > Extend labels via Voronoi (clesperanto)")
@time_slicer
@_package_ncle
def extend_labeling_via_voronoi(labels:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.extend_labeling_via_voronoi(labels)


@register_function(menu="Segmentation post-processing > Reduce labels to label edges (clesperanto)")
@time_slicer
@_package_ncle
def reduce_labels_to_label_edges(labels:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.reduce_labels_to_label_edges(labels)


@register_function(menu="Segmentation post-processing > Reduce labels to centroids (clesperanto)")
@time_slicer
@_package_ncle
def reduce_labels_to_centroids(labels:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.reduce_labels_to_centroids(labels)


@register_function(menu="Segmentation post-processing > Binary not (clesperanto)")
@time_slicer
@_package_ncle
def binary_not(labels:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.binary_not(labels)


@register_function(menu="Segmentation post-processing > Binary OR / union (clesperanto)")
@time_slicer
@_package_ncle
def binary_or(labels1:"napari.types.LabelsData", labels2:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.binary_or(labels1, labels2)


@register_function(menu="Segmentation post-processing > Binary AND / intersection (clesperanto)")
@time_slicer
@_package_ncle
def binary_and(labels1:"napari.types.LabelsData", labels2:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.binary_and(labels1, labels2)


@register_function(menu="Segmentation post-processing > Binary subtract (clesperanto)")
@time_slicer
@_package_ncle
def binary_subtract(labels1:"napari.types.LabelsData", labels2:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.binary_subtract(labels1, labels2)


@register_function(menu="Segmentation post-processing > Binary XOR (clesperanto)")
@time_slicer
@_package_ncle
def binary_xor(labels1:"napari.types.LabelsData", labels2:"napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.binary_xor(labels1, labels2)


@register_function(menu="Measurement maps > Extension ratio map (clesperanto)")
@time_slicer
@_package_ncle
def extension_ratio_map(labels:"napari.types.LabelsData") -> "napari.types.ImageData":
    return cle.extension_ratio_map(labels)


@register_function(menu="Measurement maps > Pixel count map (clesperanto)")
@time_slicer
@_package_ncle
def pixel_count_map(labels:"napari.types.LabelsData") -> "napari.types.ImageData":
    return cle.pixel_count_map(labels)


@register_function(menu="Image math > Reciprocal (clesperanto)")
@time_slicer
@_package_ncle
def reciprocal(image:"napari.types.ImageData") -> "napari.types.ImageData":
    return cle.reciprocal(image)


@register_function(menu="Image math > Absolute difference (clesperanto)")
@time_slicer
@_package_ncle
def absolute_difference(image1:"napari.types.ImageData", image2:"napari.types.ImageData") -> "napari.types.ImageData":
    return cle.absolute_difference(image1, image2)


@register_function(menu="Image math > Squared difference (clesperanto)")
@time_slicer
@_package_ncle
def squared_difference(image1:"napari.types.ImageData", image2:"napari.types.ImageData") -> "napari.types.ImageData":
    return cle.squared_difference(image1, image2)


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


@register_function(menu="Transforms > Rotate (clesperanto)")
@time_slicer
@_package_ncle
def rotate(image:"napari.types.ImageData", angle_around_x_in_degrees: float = 0, angle_around_y_in_degrees: float = 0, angle_around_z_in_degrees: float = 0, rotate_around_center:bool=True, linear_interpolation:bool=False, auto_size:bool=False) -> "napari.types.ImageData":
    return cle.rotate(image, angle_around_x_in_degrees=angle_around_x_in_degrees, angle_around_y_in_degrees=angle_around_y_in_degrees, angle_around_z_in_degrees=angle_around_z_in_degrees, rotate_around_center=rotate_around_center, linear_interpolation=linear_interpolation, auto_size=auto_size)


@register_function(menu="Transforms > Scale (clesperanto)")
@time_slicer
@_package_ncle
def scale(image:"napari.types.ImageData", factor_x: float = 0, factor_y: float = 0, factor_z: float = 0, centered:bool=False, linear_interpolation:bool=True, auto_size:bool=False) -> "napari.types.ImageData":
    return cle.scale(image, factor_x=factor_x, factor_y=factor_y, factor_z=factor_z, centered=centered, linear_interpolation=linear_interpolation, auto_size=auto_size)


@register_function(menu="Transforms > Translate (clesperanto)")
@time_slicer
@_package_ncle
def translate(image:"napari.types.ImageData", translate_x: float = 0, translate_y: float = 0, translate_z: float = 0, linear_interpolation:bool=True) -> "napari.types.ImageData":
    return cle.translate(image, translate_x=translate_x, translate_y=translate_y, translate_z=translate_z, linear_interpolation=linear_interpolation)


@register_function(menu="Transforms > Rigid transform (clesperanto)")
@time_slicer
@_package_ncle
def rigid_transform(image:"napari.types.ImageData", translate_x: float = 0, translate_y: float = 0, translate_z: float = 0, angle_around_x_in_degrees: float = 0, angle_around_y_in_degrees: float = 0, angle_around_z_in_degrees: float = 0, rotate_around_center:bool=True, linear_interpolation:bool=False, auto_size:bool=False) -> "napari.types.ImageData":
    return cle.rigid_transform(image, translate_x=translate_x, translate_y=translate_y, translate_z=translate_z, angle_around_x_in_degrees=angle_around_x_in_degrees, angle_around_y_in_degrees=angle_around_y_in_degrees, angle_around_z_in_degrees=angle_around_z_in_degrees, rotate_around_center=rotate_around_center, linear_interpolation=linear_interpolation, auto_size=auto_size)


@register_function(menu="Transforms > Sub-stack (clesperanto)")
@time_slicer
@_package_ncle
def sub_stack(image:"napari.types.ImageData", start_z:int = 0, end_z:int = 1) -> "napari.types.ImageData":
    return cle.sub_stack(image, start_z=start_z, end_z=end_z)


@register_function(menu="Transforms > Reduce stack (clesperanto)")
@time_slicer
@_package_ncle
def reduce_stack(image:"napari.types.ImageData", reduction_factor:int = 2, offset:int = 0) -> "napari.types.ImageData":
    return cle.reduce_stack(image, reduction_factor=reduction_factor, offset=offset)


@register_function(menu="Segmentation post-processing > Merge annotated touching labels (clesperanto)")
@time_slicer
@_package_ncle
def merge_annotated_touching_labels(labels:"napari.types.LabelsData", binary_annotation: "napari.types.LabelsData") -> "napari.types.LabelsData":
    return cle.merge_annotated_touching_labels(labels, binary_annotation)

