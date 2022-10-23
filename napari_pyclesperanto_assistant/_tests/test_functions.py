import numpy as np

def test_labeling_and_statistics():
    from skimage.io import imread
    image = imread("napari_pyclesperanto_assistant/data/blobs.tif")

    from napari_pyclesperanto_assistant._napari_cle_functions import  voronoi_otsu_labeling
    labels = voronoi_otsu_labeling(image, spot_sigma=3.5)

    from napari_pyclesperanto_assistant._statistics_of_labeled_pixels import statistics_of_labeled_pixels
    stats = statistics_of_labeled_pixels(image, labels)

    assert len(stats) == 65

    binary = labels >= 1

    from napari_pyclesperanto_assistant._napari_cle_functions import label
    cca = label(binary)

    assert cca.max() == 60

# def test_select_gpu():
#     from napari_pyclesperanto_assistant._gui._select_gpu import select_gpu, gpu_selector
#
#     gpu_selector("")
#     select_gpu()
#     select_gpu.device = 1
#     select_gpu()


def test_numpy_functions(make_napari_viewer):
    from napari import Viewer
    from napari.layers import Image, Labels, Layer
    from napari_pyclesperanto_assistant._convert_to_numpy import convert_to_numpy, convert_image_to_labels, \
        convert_labels_to_image, make_labels_editable, reset_brightness_contrast_selected_image_layers, \
        reset_brightness_contrast, auto_brightness_contrast, auto_brightness_contrast_all_images, \
        auto_brightness_contrast_selected_image_layers, split_stack, set_voxel_size, set_voxel_size_of_all_layers

    image = np.asarray([[[0,1], [2, 3]], [[0,1], [2, 3]]])

    viewer = make_napari_viewer()

    image_layer = viewer.add_image(image)
    labels_layer = viewer.add_labels(image)

    convert_to_numpy(image_layer)
    convert_image_to_labels(image_layer)
    convert_labels_to_image(labels_layer)
    make_labels_editable(labels_layer)
    reset_brightness_contrast(image_layer)
    auto_brightness_contrast(image_layer)
    reset_brightness_contrast_selected_image_layers(viewer)
    auto_brightness_contrast_selected_image_layers(viewer)
    auto_brightness_contrast_all_images(viewer)
    split_stack(image_layer, viewer)
    set_voxel_size(image_layer)
    set_voxel_size_of_all_layers(viewer)

    from napari_pyclesperanto_assistant._statistics_of_labeled_pixels import statistics_of_labeled_pixels
    statistics_of_labeled_pixels(image, labels_layer.data, napari_viewer=viewer)

def test_cle_functions():
    image = np.asarray([[[0, 1], [2, 3]], [[0, 1], [2, 3]]])
    labels = image.astype(int)

    from napari_pyclesperanto_assistant import (
        label,
        voronoi_otsu_labeling,
        merge_touching_labels,
        merge_labels_with_border_intensity_within_range,
        dilate_labels,
        erode_labels,
        opening_labels,
        closing_labels,
        smooth_labels,
        top_hat_box,
        eroded_otsu_labeling,
        gauss_otsu_labeling,
        difference_of_gaussian,
        laplacian_of_gaussian,
        subtract_gaussian_background,
        divide_by_gaussian_background,
        small_hessian_eigenvalue,
        large_hessian_eigenvalue,
        standard_deviation_box,
        variance_box,
        exclude_large_labels,
        exclude_small_labels,
        exclude_labels_with_map_values_out_of_range,
        exclude_labels_with_map_values_within_range,
        extend_labeling_via_voronoi,
        reduce_labels_to_label_edges,
        reduce_labels_to_centroids,
        binary_not,
        binary_or,
        binary_and,
        binary_subtract,
        binary_xor,
        extension_ratio_map,
        pixel_count_map,
        reciprocal,
        absolute_difference,
        squared_difference,
        mean_box,
        gaussian_blur
    )
    mean_box(image)
    gaussian_blur(image)
    difference_of_gaussian(image)
    laplacian_of_gaussian(image)
    subtract_gaussian_background(image)
    divide_by_gaussian_background(image)
    small_hessian_eigenvalue(image)
    large_hessian_eigenvalue(image)
    standard_deviation_box(image)
    variance_box(image)
    exclude_small_labels(labels)
    exclude_large_labels(labels)
    exclude_labels_with_map_values_out_of_range(image, labels)
    exclude_labels_with_map_values_within_range(image, labels)
    extend_labeling_via_voronoi(labels)
    reduce_labels_to_centroids(labels)
    reduce_labels_to_label_edges(labels)
    binary_not(labels)
    binary_or(labels, labels)
    binary_xor(labels, labels)
    binary_and(labels, labels)
    binary_subtract(labels, labels)
    extension_ratio_map(labels)
    pixel_count_map(labels)
    reciprocal(image)
    absolute_difference(image, image)
    squared_difference(image, image)
    label(labels)
    voronoi_otsu_labeling(image)
    merge_touching_labels(labels)
    merge_labels_with_border_intensity_within_range(image, labels)
    dilate_labels(labels)
    erode_labels(labels)
    opening_labels(labels)
    closing_labels(labels)
    smooth_labels(labels)
    top_hat_box(image)
    eroded_otsu_labeling(image)
    gauss_otsu_labeling(image)


def test_advanced_statistics(make_napari_viewer):
    image = np.asarray([[[0, 1], [2, 3]], [[0, 1], [2, 3]]])

    viewer = make_napari_viewer()

    image_layer = viewer.add_image(image)
    labels_layer = viewer.add_labels(image)

    from napari_pyclesperanto_assistant._advanced_statistics import advanced_statistics
    advanced_statistics(image, labels_layer.data, napari_viewer=viewer)

def test_plugin_interface():
    from napari_pyclesperanto_assistant._napari_plugin import napari_experimental_provide_function, \
        napari_provide_sample_data, napari_experimental_provide_dock_widget
    napari_experimental_provide_function()
    napari_provide_sample_data()
    napari_experimental_provide_dock_widget()

def test_example_data():
    from napari_pyclesperanto_assistant._napari_plugin import _load_perfect_tissue, _load_chaotic_tissue, \
        _load_orderly_tissue

    _load_orderly_tissue()
    _load_perfect_tissue()
    _load_chaotic_tissue()

