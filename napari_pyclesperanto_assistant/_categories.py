from dataclasses import dataclass, field
from typing import Any, Sequence, Tuple, Type

from napari.layers import Image, Labels, Layer
from typing_extensions import Annotated

OneKFloat = Annotated[float, {"min": -1000, "max": 1000}]
OneKInt = Annotated[int, {"min": -1000, "max": 1000}]
ImageInput = Annotated[Image, {"label": "Image"}]
LayerInput = Annotated[Layer, {"label": "Image"}]
LabelsInput = Annotated[Labels, {"label": "Labels"}]
OneKInt = Annotated[int, {"min": -1000, "max": 1000}]
global_magic_opts = {"auto_call": True}


@dataclass
class Category:
    name: str
    inputs: Sequence[Type]
    default_op: str
    output: str = "image"  # or labels
    # [(name, annotation, default), ...]
    args: Sequence[Tuple[str, Type, Any]] = field(default_factory=tuple)
    # categories
    include: Sequence[str] = field(default_factory=tuple)
    exclude: Sequence[str] = field(default_factory=tuple)


CATEGORIES = {
    "Noise removal": Category(
        name="Noise removal",
        inputs=(ImageInput,),
        default_op="gaussian_blur",
        args=[("x", OneKFloat, 1), ("y", OneKFloat, 1), ("z", OneKFloat, 0)],
        include=("filter", "denoise"),
        exclude=("combine",),
    ),
    "Background removal": Category(
        name="Background removal",
        inputs=(ImageInput,),
        default_op="top_hat_box",
        args=[("x", OneKFloat, 10), ("y", OneKFloat, 10), ("z", OneKFloat, 0)],
        include=("filter", "background removal"),
        exclude=("combine",),
    ),
    "Filter": Category(
        name="Filter",
        inputs=(ImageInput,),
        default_op="gamma_correction",
        args=[("x", OneKFloat, 1), ("y", OneKFloat, 1), ("z", OneKFloat, 0)],
        include=("filter",),
        exclude=("combine", "denoise", "background removal"),
    ),
    "Combine": Category(
        name="Combine",
        inputs=(LayerInput, LayerInput),
        default_op="binary_and",
        include=("combine",),
        exclude=("map",),
    ),
    "Binarize": Category(
        name="Binarize",
        inputs=(LayerInput,),
        default_op="threshold_otsu",
        output="labels",
        args=[
            ("radius_x", OneKInt, 1),
            ("radius_y", OneKInt, 1),
            ("radius_z", OneKInt, 0),
        ],
        include=("binarize",),
        exclude=("combine",),
    ),
    "Label": Category(
        name="Label",
        inputs=(LayerInput,),
        default_op="connected_components_labeling_box",
        output="labels",
        args=[("a", OneKFloat, 2), ("b", OneKFloat, 2)],
        include=("label",),
    ),
    "Label processing": Category(
        name="Label processing",
        inputs=(LabelsInput,),
        default_op="exclude_labels_on_edges",
        output="labels",
        args=[("min", OneKFloat, 2), ("max", OneKFloat, 100)],
        include=("label processing",),
    ),
    "Label measurements": Category(
        name="Label measurements",
        inputs=(ImageInput, LabelsInput),
        default_op="label_mean_intensity_map",
        args=[("n", float, 1)],
        include=("combine", "map"),
    ),
    "Map": Category(
        name="Map",
        inputs=(LabelsInput,),
        default_op="label_pixel_count_map",
        args=[("n", float, 1)],
        include=("label measurement", "map"),
        exclude=("combine",),
    ),
    "Mesh": Category(
        name="Mesh",
        inputs=(LabelsInput,),
        default_op="draw_mesh_between_touching_labels",
        args=[("n", float, 1)],
        include=("label measurement", "mesh"),
    ),
    "Transform": Category(
        name="Transform",
        inputs=(LayerInput,),
        default_op="sub_stack",
        output="image",  # can also be labels
        args=[
            ("a", OneKFloat, 0),
            ("b", OneKFloat, 0),
            ("c", OneKFloat, 0),
            ("d", bool, False),
            ("e", bool, False),
        ],
        include=("transform",),
    ),
    "Projection": Category(
        name="Projection",
        inputs=(LayerInput,),
        default_op="maximum_z_projection",
        output="image",  # can also be labels
        include=("projection",),
    ),
}
