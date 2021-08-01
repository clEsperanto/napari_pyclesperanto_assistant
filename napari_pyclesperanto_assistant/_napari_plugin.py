# Implementation of napari hooks according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec
from functools import partial
from pathlib import Path

from napari_plugin_engine import napari_hook_implementation

from ._categories import CATEGORIES
from ._gui import Assistant
from ._gui._category_widget import make_gui_for_category
from ._statistics_of_labeled_pixels import statistics_of_labeled_pixels
from ._convert_to_numpy import convert_to_numpy, convert_to_2d_timelapse, make_labels_editable, \
    reset_brightness_contrast, auto_brightness_contrast, split_stack, auto_brightness_contrast_all_images, \
    set_voxel_size, set_voxel_size_of_all_layers, convert_labels_to_image, convert_image_to_labels
from ._categories import attach_tooltips

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    attach_tooltips()
    return [Assistant] + [
        (partial(make_gui_for_category, category), {"name": name})
        for name, category in CATEGORIES.items()
    ]


@napari_hook_implementation
def napari_provide_sample_data():
    data = Path(__file__).parent / "data"
    return {
        "Lund": data / "Lund_000500_resampled-cropped.tif",
        "CalibZAPWfixed": data / "CalibZAPWfixed_000154_max.tif",
        "Sonneberg": data / "Sonneberg100_Resampled_RotY-40_MaxZ.tif",
        "Haase_MRT_tfl3d1": "https://zenodo.org/record/5090508/files/Haase_MRT_tfl3d1.tif?download=1",
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
        convert_to_2d_timelapse
    ]