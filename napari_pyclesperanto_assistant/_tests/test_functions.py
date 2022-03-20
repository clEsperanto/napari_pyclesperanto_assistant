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
