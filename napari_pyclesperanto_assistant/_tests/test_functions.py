import numpy as np

def test_labeling_and_statistics():
    from skimage.io import imread
    image = imread("napari_pyclesperanto_assistant/data/blobs.tif")

    from napari_pyclesperanto_assistant._napari_cle_functions import  voronoi_otsu_labeling
    labels = voronoi_otsu_labeling(image)

    from napari_pyclesperanto_assistant._statistics_of_labeled_pixels import statistics_of_labeled_pixels
    stats = statistics_of_labeled_pixels(image, labels)

    assert len(stats) == 37

    binary = labels >= 1

    from napari_pyclesperanto_assistant._napari_cle_functions import label
    cca = label(binary)

    assert cca.max() == 59

def test_select_gpu():
    from napari_pyclesperanto_assistant._gui._select_gpu import select_gpu, gpu_selector

    gpu_selector("")
    select_gpu()
    select_gpu.device = 1
    select_gpu()


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

