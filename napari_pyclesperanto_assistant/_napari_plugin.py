# Implementation of napari hooks according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec

from napari_plugin_engine import napari_hook_implementation
from pathlib import Path

from ._gui import Assistant


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return Assistant


@napari_hook_implementation
def napari_provide_sample_data():
    data = Path(__file__).parent / "data"
    return {
        "Lund": data / "Lund_000500_resampled-cropped.tif",
        "CalibZAPW": data / "CalibZAPWfixed_000154_max-16.tif",
        "Sonneberg": data / "Sonneberg100_Resampled_RotY-40_MaxZ.tif",
    }
