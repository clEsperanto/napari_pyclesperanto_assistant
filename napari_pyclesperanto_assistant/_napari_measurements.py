# Implementation of napari hooks according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec
from functools import partial

from napari_plugin_engine import napari_hook_implementation

from ._categories import CATEGORIES
from ._gui._category_widget import make_gui_for_category
from ._categories import attach_tooltips
from ._statistics_of_labeled_pixels import statistics_of_labeled_pixels


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    attach_tooltips()
    return [
        (partial(make_gui_for_category, category), {"name": name})
        for name, category in CATEGORIES.items() if "Measure" in name
    ]

@napari_hook_implementation
def napari_experimental_provide_function():
    return [
        statistics_of_labeled_pixels
    ]
