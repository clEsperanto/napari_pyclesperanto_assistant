# -----------------------------------------------------------------------------
# The user interface of the _operations is build by magicgui

import inspect
from enum import Enum
from functools import partial

import pyclesperanto_prototype as cle
from napari.layers import Image, Labels, Layer
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem
from typing_extensions import Annotated

OneKFloat = Annotated[float, {"min": -1000, "max": 1000}]
OneKInt = Annotated[int, {"min": -1000, "max": 1000}]
ImageInput = Annotated[Image, {"label": "Image"}]
LayerInput = Annotated[Layer, {"label": "Image"}]
LabelsInput = Annotated[Labels, {"label": "Labels"}]
OneKInt = Annotated[int, {"min": -1000, "max": 1000}]
global_magic_opts = {"auto_call": True}

OPERATION_NAMES = {
    "Noise removal": "denoise",
    "Background removal": "background_removal",
    "Filter": "filter",
    "Combine": "combine",
    "Transform": "transform",
    "Projection": "projection",
    "Binarize": "binarize",
    "Label": "label",
    "Label processing": "label_processing",
    "Label measurements": "label_measurements",
    "Map": "map",
    "Mesh": "mesh",
    "Measure": "measure",
}


def _call_operation_ignoring_to_many_arguments(operation, arguments):
    """
    This function is used to call an operation with three positional parameters even though
    it just takes two. Thus, we may ignore parameters entered in the GUI.
    """

    sig = inspect.signature(operation)

    count = sum(
        sig.parameters[parameter].annotation in [cle.Image, int, str, float, bool]
        for parameter in sig.parameters
    )

    if count < len(arguments):
        arguments = arguments[:count]
    return operation(*arguments)


def label_parameters(operation, parameters):
    sig = inspect.signature(operation)

    count = 0
    for parameter in sig.parameters:
        if (
            sig.parameters[parameter].annotation in [int, str, float, bool]
            and len(parameters) > count
        ):
            parameters[count].label = parameter
            parameters[count].text = parameter
            count += 1
    for i in range(count, len(parameters)):
        parameters[i].label = ""
        parameters[i].text = ""


def make_enum(name, include=(), exclude=()):
    include = list(include) + ["in assistant"]
    return Enum(
        name, {k: partial(v) for k, v in cle.operations(include, exclude).items()}
    )


Denoise = make_enum("Denoise", ("filter", "denoise"), ("combine",))
Background = make_enum("Background", ("filter", "background removal"), ("combine",))
Filter = make_enum("Filter", ("filter",), ("combine", "denoise", "background removal"))
Binarize = make_enum("Binarize", ("binarize",), ("combine",))
Combine = make_enum("Combine", ("combine",), ("map",))
Label = make_enum("Label", ("label",))
LabelProcessing = make_enum("LabelProcessing", ("label processing",))
LabelMeasurements = make_enum("LabelMeasurements", ("combine", "map"))
Mesh = make_enum("Mesh", ("label measurement", "mesh"))
Map = make_enum("Map", ("label measurement", "map"), ("combine",))
Transform = make_enum("Transform", ("transform",))
Projection = make_enum("Projection", ("projection",))


def denoise(
    input1: ImageInput,
    operation=Denoise.gaussian_blur,
    x: OneKFloat = 1,
    y: OneKFloat = 1,
    z: OneKFloat = 0,
):
    if not input1:
        return
    # execute operation
    cle_input = cle.push(input1.data)
    output = cle.create_like(cle_input)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [denoise.x, denoise.y, denoise.z])
    _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(denoise._dialog, "layer"):
        denoise._dialog.viewer.add_image(
            output, colormap=input1.colormap, translate=input1.translate
        )
    else:
        denoise._dialog.layer.data = output
        denoise._dialog.layer.name = "Result of " + operation.__name__
        denoise._dialog.layer.contrast_limits = (0, max_intensity)
        denoise._dialog.layer.translate = input1.translate


def background_removal(
    input1: ImageInput,
    operation=Background.top_hat_box,
    x: OneKFloat = 10,
    y: OneKFloat = 10,
    z: OneKFloat = 0,
):
    if not input1:
        return

    # execute operation
    cle_input = cle.push(input1.data)
    output = cle.create_like(cle_input)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(
        operation,
        [background_removal.x, background_removal.y, background_removal.z],
    )
    _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(background_removal._dialog, "layer"):
        background_removal._dialog.viewer.add_image(
            output, colormap=input1.colormap, translate=input1.translate
        )
    else:
        background_removal._dialog.layer.data = output
        background_removal._dialog.layer.name = "Result of " + operation.__name__
        background_removal._dialog.layer.contrast_limits = (0, max_intensity)
        background_removal._dialog.layer.translate = input1.translate


def filter(
    input1: ImageInput,
    operation=Filter.gamma_correction,
    x: OneKFloat = 1,
    y: OneKFloat = 1,
    z: OneKFloat = 0,
):
    if not input1:
        return
    # execute operation
    cle_input = cle.push(input1.data)
    output = cle.create_like(cle_input)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [filter.x, filter.y, filter.z])
    _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(filter._dialog, "layer"):
        filter._dialog.viewer.add_image(
            output, colormap=input1.colormap, translate=input1.translate
        )
    else:
        filter._dialog.layer.data = output
        filter._dialog.layer.name = "Result of " + operation.__name__
        filter._dialog.layer.contrast_limits = (0, max_intensity)
        filter._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def binarize(
    input1: LayerInput,
    operation=Binarize.threshold_otsu,
    radius_x: OneKInt = 1,
    radius_y: OneKInt = 1,
    radius_z: OneKInt = 0,
):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(
        operation, [binarize.radius_x, binarize.radius_y, binarize.radius_z]
    )
    _call_operation_ignoring_to_many_arguments(
        operation, [cle_input1, output, radius_x, radius_y, radius_z]
    )
    output = cle.pull(output).astype(int)

    # show result in napari
    if not hasattr(binarize._dialog, "layer"):
        binarize._dialog.viewer.add_labels(output, translate=input1.translate)
    else:
        binarize._dialog.layer.data = output
        binarize._dialog.layer.contrast_limits = (0, 1)
        binarize._dialog.layer.name = "Result of " + operation.__name__
        binarize._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def combine(
    input1: LayerInput,
    input2: LayerInput = None,
    operation=Combine.binary_and,
):
    if input1 is None:
        return

    if input2 is None:
        input2 = input1

    # execute operation
    cle_input1 = cle.push(input1.data)
    cle_input2 = cle.push(input2.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    _call_operation_ignoring_to_many_arguments(
        operation, [cle_input1, cle_input2, output]
    )
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(combine._dialog, "layer"):
        combine._dialog.viewer.add_image(
            output, colormap=input1.colormap, translate=input1.translate
        )
    else:
        combine._dialog.layer.data = output
        combine._dialog.layer.name = "Result of " + operation.__name__
        combine._dialog.layer.contrast_limits = (0, max_intensity)
        combine._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def label(
    input1: LayerInput,
    operation=Label.connected_components_labeling_box,
    a: OneKFloat = 2,
    b: OneKFloat = 2,
):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [label.a, label.b])
    output = cle.create_like(cle_input1)
    _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, a, b])
    output = cle.pull(output).astype(int)

    # show result in napari
    if not hasattr(label._dialog, "layer"):
        label._dialog.viewer.add_labels(output, translate=input1.translate)
    else:
        label._dialog.layer.data = output
        label._dialog.layer.name = "Result of " + operation.__name__
        label._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def label_processing(
    input1: LabelsInput,
    operation=LabelProcessing.exclude_labels_on_edges,
    min: OneKFloat = 0,
    max: OneKFloat = 100,
):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [label_processing.min, label_processing.max])
    _call_operation_ignoring_to_many_arguments(
        operation, [cle_input1, output, min, max]
    )
    output = cle.pull(output).astype(int)

    # show result in napari
    if not hasattr(label_processing._dialog, "layer"):
        label_processing._dialog.viewer.add_labels(output, translate=input1.translate)
    else:
        label_processing._dialog.layer.data = output
        label_processing._dialog.layer.name = "Result of " + operation.__name__
        label_processing._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def label_measurements(
    input1: ImageInput,
    input2: LabelsInput = None,
    operation=LabelMeasurements.label_mean_intensity_map,
    n: float = 1,
):
    if input1 is None:
        return

    if input2 is None:
        input2 = input1

    # execute operation
    cle_input1 = cle.push(input1.data)
    cle_input2 = cle.push(input2.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [label_measurements.n])
    _call_operation_ignoring_to_many_arguments(
        operation, [cle_input1, cle_input2, output, n]
    )
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(label_measurements._dialog, "layer"):
        label_measurements._dialog.viewer.add_image(
            output,
            colormap="turbo",
            interpolation="nearest",
            translate=input1.translate,
        )
    else:
        label_measurements._dialog.layer.data = output
        label_measurements._dialog.layer.name = "Result of " + operation.__name__
        label_measurements._dialog.layer.contrast_limits = (0, max_intensity)
        label_measurements._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def mesh(
    input1: LabelsInput,
    operation=Mesh.draw_mesh_between_touching_labels,
    n: float = 1,
):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [mesh.n])
    _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, n])
    min_intensity = cle.minimum_of_all_pixels(output)
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity - min_intensity == 0:
        max_intensity = min_intensity + 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(mesh._dialog, "layer"):
        mesh._dialog.viewer.add_image(
            output,
            colormap="green",
            blending="additive",
            translate=input1.translate,
        )
    else:
        mesh._dialog.layer.data = output
        mesh._dialog.layer.name = "Result of " + operation.__name__
        mesh._dialog.layer.contrast_limits = (min_intensity, max_intensity)
        mesh._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
def map(
    input1: LabelsInput,
    operation=Map.label_pixel_count_map,
    n: float = 1,
):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = cle.create_like(cle_input1)
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(operation, [map.n])
    _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, n])
    max_intensity = cle.maximum_of_all_pixels(output)
    if max_intensity == 0:
        max_intensity = 1  # prevent division by zero in vispy
    output = cle.pull(output)

    # show result in napari
    if not hasattr(map._dialog, "layer"):
        map._dialog.viewer.add_image(
            output,
            colormap="turbo",
            interpolation="nearest",
            translate=input1.translate,
        )
    else:
        map._dialog.layer.data = output
        map._dialog.layer.name = "Result of " + operation.__name__
        map._dialog.layer.contrast_limits = (0, max_intensity)
        map._dialog.layer.translate = input1.translate


# -----------------------------------------------------------------------------
# A special case of ooperation is measurement: it results in a table instead of
# an image


def measure(input1: ImageInput = None, labels: LabelsInput = None):
    if input1 is not None and labels is not None:
        from skimage.measure import regionprops_table

        table = regionprops_table(
            labels.data.astype(int),
            intensity_image=input1.data,
            properties=("area", "centroid", "mean_intensity"),
        )
        dock_widget = table_to_widget(table)
        labels._dialog.layer.viewer.window.add_dock_widget(dock_widget, area="right")


def table_to_widget(table: dict) -> QTableWidget:
    view = QTableWidget(len(next(iter(table.values()))), len(table))
    for i, column in enumerate(table.keys()):
        view.setItem(0, i, QTableWidgetItem(column))
        for j, value in enumerate(table.get(column)):
            view.setItem(j + 1, i, QTableWidgetItem(str(value)))
    return view


# -----------------------------------------------------------------------------
def transform(
    input1: LayerInput,
    operation=Transform.sub_stack,
    a: OneKFloat = 0,
    b: OneKFloat = 0,
    c: OneKFloat = 0,
    d: bool = False,
    e: bool = False,
):
    if input1 is None:
        return

    # determine shift; todo: to this in a generic way
    import numpy as np

    translate = np.copy(input1.translate)
    if operation.name == cle.sub_stack.__name__:
        translate[0] += a  # a corresponds to start_z
    elif operation.name == cle.reduce_stack.__name__:
        translate[0] += b  # b corresponds to offset

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = None
    operation = cle.operation(operation.name)
    # update GUI
    label_parameters(
        operation, [transform.a, transform.b, transform.c, transform.d, transform.e]
    )
    output = _call_operation_ignoring_to_many_arguments(
        operation, [cle_input1, output, a, b, c, d, e]
    )
    output = cle.pull(output).astype(int)

    # show result in napari
    if not hasattr(transform._dialog, "layer"):
        if isinstance(input1, Labels):
            transform._dialog.viewer.add_labels(output, translate=translate)
        else:
            transform._dialog.viewer.add_image(output, translate=translate)
    else:
        transform._dialog.layer.data = output
        transform._dialog.layer.contrast_limits = input1.contrast_limits
        transform._dialog.layer.name = "Result of " + operation.__name__
        transform._dialog.layer.translate = translate


# -----------------------------------------------------------------------------
def projection(input1: LayerInput, operation=Projection.maximum_z_projection):
    if input1 is None:
        return

    # execute operation
    cle_input1 = cle.push(input1.data)
    output = None
    operation = cle.operation(operation.name)
    output = _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output])
    output = cle.pull(output).astype(int)

    # show result in napari
    if not hasattr(projection._dialog, "layer"):
        if isinstance(input1, Labels):
            projection._dialog.viewer.add_labels(
                output, translate=input1.translate[1:3]
            )
        else:
            projection._dialog.viewer.add_image(output, translate=input1.translate[1:3])
    else:
        projection._dialog.layer.data = output
        projection._dialog.layer.contrast_limits = input1.contrast_limits
        projection._dialog.layer.name = "Result of " + operation.__name__
        projection._dialog.layer.translate = input1.translate[1:3]
