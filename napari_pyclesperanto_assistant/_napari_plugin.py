# Implementation of napari hooks according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec
from functools import partial
from pathlib import Path

from napari_plugin_engine import napari_hook_implementation

from ._categories import CATEGORIES
from ._gui import Assistant
from ._gui._category_widget import make_gui_for_category
from ._statistics_of_labeled_pixels import statistics_of_labeled_pixels
from ._convert_to_numpy import convert_to_numpy, make_labels_editable, \
    reset_brightness_contrast, auto_brightness_contrast, split_stack, auto_brightness_contrast_all_images, \
    set_voxel_size, set_voxel_size_of_all_layers, convert_labels_to_image, convert_image_to_labels
from ._napari_cle_functions import label, voronoi_otsu_labeling
from ._categories import attach_tooltips
from skimage.io import imread

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    attach_tooltips()
    return [Assistant] + [
        (partial(make_gui_for_category, category), {"name": name})
        for name, category in CATEGORIES.items()
    ]

def _load_Lund():
    return [(imread("https://github.com/clEsperanto/clesperanto_example_data/raw/main/Lund_000500_resampled-cropped.tif"), {'name': 'Lund'})]

def _load_CalibZAPWfixed():
    return [(imread("https://github.com/clEsperanto/clesperanto_example_data/raw/main/CalibZAPWfixed_000154_max.tif"), {'name': 'CalibZAPWfixed'})]

def _load_Sonneberg():
    return [(imread("https://github.com/clEsperanto/clesperanto_example_data/raw/main/Sonneberg100_Resampled_RotY-40_MaxZ.tif"), {'name': 'Sonneberg'})]

def _load_Haase_MRT_tfl3d1():
    return [(imread("https://github.com/clEsperanto/clesperanto_example_data/raw/main/Haase_MRT_tfl3d1.tif"), {'name': 'Haase MRT'})]

def _load_Pixel_cat():
    return [(imread("https://github.com/clEsperanto/clesperanto_example_data/raw/main/pixel_cat.tif"), {'name': 'Pixel cat'})]

def _load_perfect_tissue():
    import pyclesperanto_prototype as cle
    return [(cle.artificial_tissue_2d(random_sigma_x=1, random_sigma_y=0), {'name': 'Artifical perfect tissue (pos sigma 0)'})]

def _load_orderly_tissue():
    import pyclesperanto_prototype as cle
    return [(cle.artificial_tissue_2d(random_sigma_x=1, random_sigma_y=2), {'name': 'Artifical orderly tissue (pos sigma 2)'})]

def _load_chaotic_tissue():
    import pyclesperanto_prototype as cle
    return [(cle.artificial_tissue_2d(random_sigma_x=1, random_sigma_y=8), {'name': 'Artifical chaotic tissue (pos sigma 8)'})]

@napari_hook_implementation
def napari_provide_sample_data():
    data = Path(__file__).parent / "data"
    return {
        "Lund": _load_Lund,
        "CalibZAPWfixed": _load_CalibZAPWfixed,
        "Sonneberg": _load_Sonneberg,
        "Haase_MRT_tfl3d1": _load_Haase_MRT_tfl3d1,
        "Pixel (cat)": _load_Pixel_cat,
        "Artificial perfect tissue": _load_perfect_tissue,
        "Artificial orderly tissue": _load_orderly_tissue,
        "Artificial chaotic tissue": _load_chaotic_tissue,
        "Blobs (from ImageJ)": data / "blobs.tif",
    }


@napari_hook_implementation
def napari_experimental_provide_function():
    return [
        statistics_of_labeled_pixels,
        make_labels_editable,
        auto_brightness_contrast,
        auto_brightness_contrast_all_images,
        reset_brightness_contrast,
        split_stack,
        set_voxel_size,
        set_voxel_size_of_all_layers,
        convert_image_to_labels,
        convert_labels_to_image,
        convert_to_numpy,
        label,
        voronoi_otsu_labeling
    ]