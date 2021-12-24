from dataclasses import dataclass, field
from typing import Any, Sequence, Tuple, Type

import numpy as np
import napari
from napari.layers import Image, Labels, Layer
from typing_extensions import Annotated
import inspect

ImageInput = Annotated[Image, {"label": "Image"}]
LayerInput = Annotated[Layer, {"label": "Image or labels"}]
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
        default_values=[1, 1],
        tools_menu="Image math",
    ),
    "Transform": Category(
        name="Transform",
        description="Apply spatial transformation to images.",
        inputs=(LayerInput,),
        default_op="sub_stack (clesperanto)",
        output="image",  # can also be labels
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
        choices = operations_in_menu(c)
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

    #print(allowed_types)
    return result


@lru_cache(maxsize=1)
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

def operations_in_menu(category, search_string: str = None):
    menu_name = category.tools_menu
    choices = filter_operations(menu_name)
    if search_string is not None and len(search_string) > 0:
        choices = [c for c in choices if search_string in c.lower()]
    choices = [c.split(">")[1].strip() for c in choices]
    choices = sorted(choices, key=str.casefold)

    #print("\n", category.name)

    # check if the image parameters fit
    result = []
    for name in choices:
        func = find_function(name)
        sig = inspect.signature(func)

        # count number of image-like parameters and compare to category
        num_image_parameters_in_category = len(category.inputs)
        num_image_parameters_in_function = 0
        for i, key in enumerate(list(sig.parameters.keys())):
            type_annotation = str(sig.parameters[key].annotation)

            if "NewType.<locals>.new_type" in type_annotation or \
                "Image" in type_annotation or \
                "LabelsData" in type_annotation or \
                "LayerData" in type_annotation:
                num_image_parameters_in_function = num_image_parameters_in_function + 1
            else:
                break

        if "pyclesperanto_prototype" in func.__module__:
            # all clesperanto function have an output image which we don't pass
            num_image_parameters_in_function -= 1

        # only keep the function in this category if it matches
        if num_image_parameters_in_category == num_image_parameters_in_function:
            result.append(name)
        #else:
            #print(name, num_image_parameters_in_category, num_image_parameters_in_function)

    return result


def find_function(op_name):
    all_ops = all_operations()
    cle_function = None
    for k, f in all_ops.items():
        if op_name in k:
            cle_function = f
    if cle_function is None:
        print("No function found for", op_name)
    return cle_function


def filter_categories(search_string:str=""):
    if search_string is None or len(search_string) == 0:
        return CATEGORIES

    from copy import copy

    result = {}
    for k, c in CATEGORIES.items():
        if not callable(c):
            if search_string in c.tool_tip.lower():
                new_c = copy(c)
                result[k] = new_c

    for k, c in result.items():
        choices = operations_in_menu(c, search_string)
        c.tool_tip = c.description + "\n\nOperations:\n* " + "\n* ".join(choices).replace("_", " ")

    return result
