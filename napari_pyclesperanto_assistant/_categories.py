from dataclasses import dataclass, field
from typing import Any, Sequence, Tuple, Type

import numpy as np
from napari.layers import Image, Labels, Layer
from typing_extensions import Annotated

FloatRange = Annotated[float, {"min": np.finfo(np.float32).min, "max": np.finfo(np.float32).max}]
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
        default_op="gaussian_blur",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        include=("filter", "denoise"),
        exclude=("combine",),
        tools_menu="Filtering",
    ),
    "Remove background": Category(
        name="Remove background",
        description="Remove background intensity, e.g. caused\nby out-of-focus light or uneven illumination.",
        inputs=(ImageInput,),
        default_op="top_hat_box",
        args=[
            ("x", FloatRange, 10),
            ("y", FloatRange, 10),
            ("z", FloatRange, 0)
        ],
        include=("filter", "background removal"),
        exclude=("combine",),
        tools_menu="Filtering",
    ),
    "Filter": Category(
        name="Filter",
        description="Filter images, e.g. to adjust gamma or detect edges.",
        inputs=(ImageInput,),
        default_op="gamma_correction",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        include=("filter",),
        exclude=("combine", "denoise", "background removal", "binary processing"),
        tools_menu="Filtering",
    ),
    "Combine": Category(
        name="Combine",
        description="Combine images using pixel-wise mathematical operations.",
        inputs=(LayerInput, LayerInput),
        default_op="add_images",
        include=("combine",),
        exclude=("map",),
        args=[
            ("a", FloatRange, 1),
            ("b", FloatRange, 1),
        ],
        tools_menu="Utilities",
    ),
    "Transform": Category(
        name="Transform",
        description="Apply spatial transformation to images.",
        inputs=(LayerInput,),
        default_op="sub_stack",
        output="image",  # can also be labels
        args=[
            ("a", FloatRange, 0),
            ("b", FloatRange, 0),
            ("c", FloatRange, 0),
            ("d", bool, False),
            ("e", bool, False),
        ],
        include=("transform",),
        tools_menu="Transform",
    ),
    "Projection": Category(
        name="Projection",
        description="Reduce dimensionality of images\nfrom three to two dimensions.",
        inputs=(LayerInput,),
        default_op="maximum_z_projection",
        args=[
            ("rx", PositiveFloatRange, 1),
            ("ry", PositiveFloatRange, 1),
            ("s", PositiveFloatRange, 1),
        ],
        output="image",  # can also be labels
        include=("projection",),
        tools_menu="Transform",
    ),
    "Binarize": Category(
        name="Binarize",
        description="Turn images into binary images.",
        inputs=(LayerInput,),
        default_op="threshold_otsu",
        output="labels",
        args=[
            ("radius_x", PositiveFloatRange, 1),
            ("radius_y", PositiveFloatRange, 1),
            ("radius_z", PositiveFloatRange, 0),
        ],
        include=("binarize",),
        exclude=("combine",),
        tools_menu="Segmentation",
    ),
    "Label": Category(
        name="Label",
        description="Turn images or binary images into\nlabel images by labeling objects.",
        inputs=(LayerInput,),
        default_op="voronoi_otsu_labeling",
        output="labels",
        args=[
            ("a", PositiveFloatRange, 2),
            ("b", PositiveFloatRange, 2)
        ],
        include=("label",),
        tools_menu="Segmentation",
    ),
    "Process labels": Category(
        name="Process labels",
        description="Process label images to improve\nby changing their shape and/or removing\nobjects which don't fulfill certain conditions.",
        inputs=(LabelsInput,),
        default_op="exclude_labels_on_edges",
        output="labels",
        args=[
            ("min", PositiveFloatRange, 2),
            ("max", PositiveFloatRange, 100)
        ],
        include=("label processing",),
        tools_menu="Segmentation",
    ),
    "Measure labels": Category(
        name="Measure labels",
        description="Measure and visualize spatial\nfeatures of labeled objects.",
        inputs=(LabelsInput,),
        default_op="pixel_count_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
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
        default_op="mean_intensity_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
        include=("combine","label measurement", "map"),
        color_map="turbo",
        blending="translucent",
        tools_menu="Measurement",
    ),
    "Mesh": Category(
        name="Mesh",
        description="Draw connectivity meshes between\ncentroids of labeled objects.",
        inputs=(LabelsInput,),
        default_op="draw_mesh_between_touching_labels",
        args=[
            ("n", PositiveFloatRange, 1)
        ],
        include=("label measurement", "mesh"),
        color_map="green",
        blending="additive",
        tools_menu="Visualization",
    ),
    "Label neighbor filters": Category(
        name="Label neighbor filters",
        description="Process values associated with labeled objects\naccording to the neighborhood-graph of the labels.",
        inputs=(ImageInput, LabelsInput),
        default_op="mean_of_n_nearest_neighbors_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 100),
        ],
        include=("neighbor",),
        color_map="turbo",
        blending="translucent",
        tools_menu="Segmentation",
    ),
}

def attach_tooltips():
    # attach tooltips
    import pyclesperanto_prototype as cle
    for k, c in CATEGORIES.items():
        choices = list(cle.operations(['in assistant'] + list(c.include), c.exclude))
        # temporary workaround: remove entries that start with "label_", those have been renamed in pyclesperanto
        # and are only there for backwards compatibility
        choices = list([c for c in choices if not c.startswith('label_')])
        c.tool_tip = c.description + "\n\nOperations:\n* " + "\n* ".join(choices).replace("_", " ")
