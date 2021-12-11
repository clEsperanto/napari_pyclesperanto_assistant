from dataclasses import dataclass, field
from typing import Any, Sequence, Tuple, Type

import numpy as np
import napari
from napari.layers import Image, Labels, Layer
from typing_extensions import Annotated

FloatRange = Annotated[float, {"min": np.finfo(np.float32).min, "max": np.finfo(np.float32).max}]
BoolType = Annotated[bool, {}]
StringType = Annotated[str, {}]
PositiveFloatRange = Annotated[float, {"min": 0, "max": np.finfo(np.float32).max}]
ImageInput = Annotated[Image, {"label": "Image"}]
LayerInput = Annotated[Layer, {"label": "Image"}]
LabelsInput = Annotated[Labels, {"label": "Labels"}]
global_magic_opts = {"auto_call": True}


@dataclass
class Category:
    name: str
    description: str
    inputs: Sequence[Type]
    default_op: str
    default_values : Sequence[float]
    output: str = "image"  # or labels
    # [(name, annotation, default), ...]
    args: Sequence[Tuple[str, Type, Any]] = field(default_factory=tuple)
    # categories
    include: Sequence[str] = field(default_factory=tuple)
    exclude: Sequence[str] = field(default_factory=tuple)
    # visualization
    color_map : str = "gray"
    blending : str = "translucent"
    tool_tip : str = None
    tools_menu : str = None


CATEGORIES = {
    "Remove noise": Category(
        name="Removal noise",
        description="Remove noise from images, e.g. by local averaging and blurring.",
        inputs=(ImageInput,),
        default_op="gaussian_blur (clesperanto)",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        default_values=[1, 1, 0],
        include=("filter", "denoise"),
        exclude=("combine",),
        tools_menu="Filtering / noise removal",
    ),
    "Remove background": Category(
        name="Remove background",
        description="Remove background intensity, e.g. caused\nby out-of-focus light or uneven illumination.",
        inputs=(ImageInput,),
        default_op="top_hat_box (clesperanto)",
        args=[
            ("x", FloatRange, 10),
            ("y", FloatRange, 10),
            ("z", FloatRange, 0)
        ],
        default_values=[10, 10, 0],
        include=("filter", "background removal"),
        exclude=("combine",),
        tools_menu="Filtering / background removal",
    ),
    "Filter": Category(
        name="Filter",
        description="Filter images, e.g. to adjust gamma or detect edges.",
        inputs=(ImageInput,),
        default_op="gamma_correction (clesperanto)",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        default_values=[1, 1, 0],
        include=("filter",),
        exclude=("combine", "denoise", "background removal", "binary processing"),
        tools_menu="Filtering",
    ),
    "Combine": Category(
        name="Combine",
        description="Combine images using pixel-wise mathematical operations.",
        inputs=(LayerInput, LayerInput),
        default_op="add_images (clesperanto)",
        include=("combine",),
        exclude=("map",),
        args=[
            ("a", FloatRange, 1),
            ("b", FloatRange, 1),
        ],
        default_values=[1, 1],
        tools_menu="Image math",
    ),
    "Transform": Category(
        name="Transform",
        description="Apply spatial transformation to images.",
        inputs=(LayerInput,),
        default_op="sub_stack (clesperanto)",
        output="image",  # can also be labels
        args=[
            ("a", FloatRange, 0),
            ("b", FloatRange, 0),
            ("c", FloatRange, 0),
            ("d", bool, False),
            ("e", bool, False),
        ],
        default_values=[0, 0, 0, 1, 1],
        include=("transform",),
        exclude=("combine",),
        tools_menu="Transform",
    ),
    "Projection": Category(
        name="Projection",
        description="Reduce dimensionality of images\nfrom three to two dimensions.",
        inputs=(LayerInput,),
        default_op="maximum_z_projection (clesperanto)",
        args=[
            ("rx", PositiveFloatRange, 1),
            ("ry", PositiveFloatRange, 1),
            ("s", PositiveFloatRange, 1),
        ],
        default_values=[1, 1, 1],
        output="image",  # can also be labels
        include=("projection",),
        tools_menu="Projection",
    ),
    "Binarize": Category(
        name="Binarize",
        description="Turn images into binary images.",
        inputs=(LayerInput,),
        default_op="threshold_otsu (clesperanto)",
        output="labels",
        args=[
            ("radius_x", PositiveFloatRange, 1),
            ("radius_y", PositiveFloatRange, 1),
            ("radius_z", PositiveFloatRange, 0),
        ],
        default_values=[1, 1, 0],
        include=("binarize",),
        exclude=("combine",),
        tools_menu="Segmentation / binarization",
    ),
    "Label": Category(
        name="Label",
        description="Turn images or binary images into\nlabel images by labeling objects.",
        inputs=(LayerInput,),
        default_op="voronoi_otsu_labeling (clesperanto)",
        output="labels",
        args=[
            ("a", PositiveFloatRange, 2),
            ("b", PositiveFloatRange, 2)
        ],
        default_values=[2, 2],
        include=("label",),
        tools_menu="Segmentation / labeling",
    ),
    "Process labels": Category(
        name="Process labels",
        description="Process label images to improve\nby changing their shape and/or removing\nobjects which don't fulfill certain conditions.",
        inputs=(LabelsInput,),
        default_op="exclude_labels_on_edges (clesperanto)",
        output="labels",
        args=[
            ("min", PositiveFloatRange, 2),
            ("max", PositiveFloatRange, 100)
        ],
        default_values=[2, 100],
        include=("label processing",),
        exclude=("combine",),
        tools_menu="Segmentation post-processing",
    ),
    "Measure labels": Category(
        name="Measure labels",
        description="Measure and visualize spatial\nfeatures of labeled objects.",
        inputs=(LabelsInput,),
        default_op="pixel_count_map (clesperanto)",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
        default_values=[1, 1],
        include=("label measurement", "map"),
        exclude=("combine",),
        color_map="turbo",
        blending="translucent",
        tools_menu="Measurement",
    ),
    "Measure labeled image": Category(
        name="Measure labeled image",
        description="Measure and visualize intensity-based\nfeatures of labeled objects.",
        inputs=(ImageInput, LabelsInput),
        default_op="mean_intensity_map (clesperanto)",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
        default_values=[1, 1],
        include=("combine","label measurement", "map",),
        exclude=("label comparison",),
        color_map="turbo",
        blending="translucent",
        tools_menu="Measurement",
    ),
    "Compare label images": Category(
        name="Compare label images",
        description="Measure and visualize overlap and \nnonzero pixel count/ratio of labeled \nobjects in two label images.",
        inputs=(LabelsInput, LabelsInput),
        default_op="label_overlap_count_map (clesperanto)",
        args=[],
        default_values=[],
        include=("combine","label measurement", "map", "label comparison",),
        color_map="turbo",
        blending="translucent",
        tools_menu="Measurement",
    ),
    "Mesh": Category(
        name="Mesh",
        description="Draw connectivity meshes between\ncentroids of labeled objects.",
        inputs=(LabelsInput,),
        default_op="draw_mesh_between_touching_labels (clesperanto)",
        args=[
            ("n", PositiveFloatRange, 1)
        ],
        default_values=[1],
        include=("label measurement", "mesh"),
        color_map="green",
        blending="additive",
        tools_menu="Visualization",
    ),
    "Label neighbor filters": Category(
        name="Label neighbor filters",
        description="Process values associated with labeled objects\naccording to the neighborhood-graph of the labels.",
        inputs=(ImageInput, LabelsInput),
        default_op="mean_of_n_nearest_neighbors_map (clesperanto)",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 100),
        ],
        default_values=[1, 100],
        include=("neighbor",),
        color_map="turbo",
        blending="translucent",
        tools_menu="Label neighbor filters",
    ),
}



def attach_tooltips():
    # attach tooltips
    for k, c in CATEGORIES.items():
        choices = operations_in_menu(c.tools_menu)
        c.tool_tip = c.description + "\n\nOperations:\n* " + "\n* ".join(choices).replace("_", " ")

from functools import lru_cache

def collect_cle():
    import pyclesperanto_prototype as cle
    result = {}

    for k, c in CATEGORIES.items():
        if not callable(c):
            choices = cle.operations(['in assistant'] + list(c.include), c.exclude)
            for choice, func in choices.items():
                result[c.tools_menu + ">" + choice + " (clesperanto)"] = func

    return result


def collect_tools():
    from napari_tools_menu import ToolsMenu
    import inspect

    allowed_types = ["napari.types.LabelsData", "napari.types.ImageData", "int", "float", "str", "bool",
                     "napari.viewer.Viewer", "napari.Viewer"]
    allowed_types = allowed_types + ["<class '" + t + "'>" for t in allowed_types]

    result = {}
    for k, v in ToolsMenu.menus.items():
        typ = v[1]
        if typ == "function":
            f = v[0]
            sig = inspect.signature(f)

            # all parameters must be images, labels, int, float or str
            skip = False
            for i, key in enumerate(list(sig.parameters.keys())):
                type_annotation = str(sig.parameters[key].annotation)
                if not "function NewType.<locals>.new_type" in type_annotation:
                    if type_annotation not in allowed_types:
                        #print("Skip", k, "because", str(type_annotation), "not in allowed types")
                        skip = True
                        break
            if skip:
                continue

            # return type must be image or label_image
            if sig.return_annotation not in [napari.types.LabelsData, "napari.types.LabelsData", napari.types.ImageData, "napari.types.ImageData"]:
                continue

            result[k] = f

    print(allowed_types)
    return result


@lru_cache
def all_operations():
    cle_ops = collect_cle()
    tools_ops = collect_tools()
    all_ops = {**cle_ops, **tools_ops}
    return all_ops

def filter_operations(menu_name):
    result = {}
    for k,v in all_operations().items():
        if menu_name in k:
            result[k] = v
    return result

def operations_in_menu(menu_name):
    choices = filter_operations(menu_name)
    choices = [c.split(">")[1] for c in choices]
    choices = sorted(choices, key=str.casefold)
    return choices