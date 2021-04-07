
# -----------------------------------------------------------------------------
# The user interface of the _operations is build by magicgui
from typing import Union

from qtpy.QtWidgets import QTableWidget, QTableWidgetItem
from magicgui import magicgui
from napari.layers import Image, Labels, Layer
import pyclesperanto_prototype as cle

plus_minus_1k = {'min': -1000, 'max': 1000}
plus_10k = {'min': 0, 'max': 10000}

def _call_operation_ignoring_to_many_arguments(operation, arguments):
    """
    This function is used to call an operation with three positional parameters even though it just takes two. Thus,
    we may ignore parameters entered in the GUI.
    """

    import inspect
    sig = inspect.signature(operation)

    count = 0
    for parameter in sig.parameters:
        if sig.parameters[parameter].annotation in [cle.Image, int, str, float, bool]:
            count = count + 1

    if count < len(arguments):
        arguments = arguments[:count]
    return operation(*arguments)

def label_parameters(operation, parameters):
    import inspect
    sig = inspect.signature(operation)

    count = 0
    for parameter in sig.parameters:
        if sig.parameters[parameter].annotation in [int, str, float, bool]:
            if len(parameters) > count:
                parameters[count].label = parameter
                parameters[count].text = parameter
                count = count + 1
    for i in range(count, len(parameters)):
        parameters[i].label = ""
        parameters[i].text = ""

@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['filter', 'denoise','in assistant'], must_not_have_categories=['combine']).keys()},
    x=plus_minus_1k,
    y=plus_minus_1k,
    z=plus_minus_1k,
)
def denoise(input1: Image, operation_name: str = cle.gaussian_blur.__name__, x: float = 1, y: float = 1, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [denoise.x, denoise.y, denoise.z])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(denoise.self, 'layer'):
            denoise.self.viewer.add_image(output, colormap=input1.colormap, translate=input1.translate)
        else:
            denoise.self.layer.data = output
            denoise.self.layer.name = "Result of " + operation.__name__
            denoise.self.layer.contrast_limits=(0, max_intensity)
            denoise.self.layer.translate = input1.translate

@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['filter', 'background removal','in assistant'], must_not_have_categories=['combine']).keys()},
    x=plus_minus_1k,
    y=plus_minus_1k,
    z=plus_minus_1k,
)
def background_removal(input1: Image, operation_name: str = cle.top_hat_box.__name__, x: float = 10, y: float = 10, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [background_removal.x, background_removal.y, background_removal.z])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(background_removal.self, 'layer'):
            background_removal.self.viewer.add_image(output, colormap=input1.colormap, translate=input1.translate)
        else:
            background_removal.self.layer.data = output
            background_removal.self.layer.name = "Result of " + operation.__name__
            background_removal.self.layer.contrast_limits=(0, max_intensity)
            background_removal.self.layer.translate = input1.translate

@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['filter', 'in assistant'], must_not_have_categories=['combine', 'denoise', 'background removal']).keys()},
    x=plus_minus_1k,
    y=plus_minus_1k,
    z=plus_minus_1k,
)
def filter(input1: Image, operation_name: str = cle.gamma_correction.__name__, x: float = 1, y: float = 1, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [filter.x, filter.y, filter.z])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input, output, x, y, z])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(filter.self, 'layer'):
            filter.self.viewer.add_image(output, colormap=input1.colormap, translate=input1.translate)
        else:
            filter.self.layer.data = output
            filter.self.layer.name = "Result of " + operation.__name__
            filter.self.layer.contrast_limits=(0, max_intensity)
            filter.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['binarize', 'in assistant'], must_not_have_categories=['combine']).keys()},
    radius_x=plus_minus_1k,
    radius_y=plus_minus_1k,
    radius_z=plus_minus_1k
)
def binarize(input1: Layer, operation_name : str = cle.threshold_otsu.__name__, radius_x : int = 1, radius_y : int = 1, radius_z : int = 0):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [binarize.radius_x, binarize.radius_y, binarize.radius_z])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, radius_x, radius_y, radius_z])
        output = cle.pull(output).astype(int)

        # show result in napari
        if not hasattr(binarize.self, 'layer'):
            binarize.self.viewer.add_labels(output, translate=input1.translate)
        else:
            binarize.self.layer.data = output
            binarize.self.layer.contrast_limits = (0, 1)
            binarize.self.layer.name = "Result of " + operation.__name__
            binarize.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image 1'},
    input2={'label':'Image 2'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['combine', 'in assistant'], must_not_have_categories=['map']).keys()}
)
def combine(input1: Layer, input2: Layer = None, operation_name: str = cle.binary_and.__name__):
    if input1 is not None:
        if (input2 is None):
            input2 = input1

        # execute operation
        cle_input1 = cle.push(input1.data)
        cle_input2 = cle.push(input2.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, cle_input2, output])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(combine.self, 'layer'):
            combine.self.viewer.add_image(output, colormap=input1.colormap, translate=input1.translate)
        else:
            combine.self.layer.data = output
            combine.self.layer.name = "Result of " + operation.__name__
            combine.self.layer.contrast_limits=(0, max_intensity)
            combine.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['label', 'in assistant']).keys()},
    a=plus_minus_1k,
    b=plus_minus_1k
)
def label(input1: Layer, operation_name: str = cle.connected_components_labeling_box.__name__, a : float = 2, b : float = 2):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [label.a, label.b])
        output = cle.create_like(cle_input1)
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, a, b])
        output = cle.pull(output).astype(int)

        # show result in napari
        if not hasattr(label.self, 'layer'):
            label.self.viewer.add_labels(output, translate=input1.translate)
        else:
            label.self.layer.data = output
            label.self.layer.name = "Result of " + operation.__name__
            label.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Labels'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['label processing', 'in assistant']).keys()},
    min = plus_minus_1k,
    max = plus_minus_1k
)
def label_processing(input1: Labels, operation_name: str = cle.exclude_labels_on_edges.__name__, min: float=0, max:float=100):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [label_processing.min, label_processing.max])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, min, max])
        output = cle.pull(output).astype(int)

        # show result in napari
        if not hasattr(label_processing.self, 'layer'):
            label_processing.self.viewer.add_labels(output, translate=input1.translate)
        else:
            label_processing.self.layer.data = output
            label_processing.self.layer.name = "Result of " + operation.__name__
            label_processing.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    input2={'label':'Labels'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['combine', 'map', 'in assistant']).keys()}
)
def label_measurements(input1: Image, input2: Labels = None, operation_name: str = cle.label_mean_intensity_map.__name__, n : float = 1):
    if input1 is not None:
        if (input2 is None):
            input2 = input1

        # execute operation
        cle_input1 = cle.push(input1.data)
        cle_input2 = cle.push(input2.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [label_measurements.n])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, cle_input2, output, n])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(label_measurements.self, 'layer'):
            label_measurements.self.viewer.add_image(output, colormap='turbo', interpolation='nearest', translate=input1.translate)
        else:
            label_measurements.self.layer.data = output
            label_measurements.self.layer.name = "Result of " + operation.__name__
            label_measurements.self.layer.contrast_limits=(0, max_intensity)
            label_measurements.self.layer.translate = input1.translate


# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label': 'Labels'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['label measurement', 'mesh', 'in assistant'], must_not_have_categories=["combine"]).keys()},
    n = {'min': 0, 'max': 1000}
)
def mesh(input1: Labels, operation_name : str = cle.draw_mesh_between_touching_labels.__name__, n : float = 1):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [mesh.n])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, n])
        min_intensity = cle.minimum_of_all_pixels(output)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity - min_intensity == 0:
            max_intensity = min_intensity + 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(mesh.self, 'layer'):
            mesh.self.viewer.add_image(output, colormap='green', blending='additive', translate=input1.translate)
        else:
            mesh.self.layer.data = output
            mesh.self.layer.name = "Result of " + operation.__name__
            mesh.self.layer.contrast_limits=(min_intensity, max_intensity)
            mesh.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Labels'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['label measurement', 'map', 'in assistant'], must_not_have_categories=["combine"]).keys()},
    n = {'min': 0, 'max': 1000}
)
def map(input1: Labels, operation_name: str = cle.label_pixel_count_map.__name__, n : float = 1):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [map.n])
        _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, n])
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull(output)

        # show result in napari
        if not hasattr(map.self, 'layer'):
            map.self.viewer.add_image(output, colormap='turbo', interpolation='nearest', translate=input1.translate)
        else:
            map.self.layer.data = output
            map.self.layer.name = "Result of " + operation.__name__
            map.self.layer.contrast_limits=(0, max_intensity)
            map.self.layer.translate = input1.translate

# -----------------------------------------------------------------------------
# A special case of ooperation is measurement: it results in a table instead of
# an image
@magicgui(
    layout='vertical',
    input1={'label': 'Image'},
    labels={'label': 'Labels'},
    call_button="Measure")
def measure(input1: Image = None, labels : Labels = None):
    if input1 is not None and labels is not None:
        from skimage.measure import regionprops_table
        table = regionprops_table(labels.data.astype(int), intensity_image=input1.data, properties=('area', 'centroid', 'mean_intensity'))
        dock_widget = table_to_widget(table)
        labels.self.layer.viewer.window.add_dock_widget(dock_widget, area='right')

def table_to_widget(table : dict) -> QTableWidget:
    view = QTableWidget(len(next(iter(table.values()))), len(table))
    for i, column in enumerate(table.keys()):
        view.setItem(0, i, QTableWidgetItem(column))
        for j, value in enumerate(table.get(column)):
            view.setItem(j + 1, i,  QTableWidgetItem(str(value)))
    return view

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['transform', 'in assistant']).keys()},
    a=plus_minus_1k,
    b=plus_minus_1k,
    c=plus_minus_1k
)
def transform(input1: Layer, operation_name : str = cle.sub_stack.__name__, a : float = 0, b : float = 0, c : float = 0, d : bool = False, e : bool = False):
    if input1 is not None:
        # determine shift; todo: to this in a generic way
        translate = input1.translate
        if operation_name == cle.sub_stack.__name__:
            translate = [input1.translate[0] + a, input1.translate[1], input1.translate[2]] # a corresponds to start_z
        elif operation_name == cle.reduce_stack.__name__:
            translate = [input1.translate[0] + b, input1.translate[1], input1.translate[2]] # b corresponds to offset

        # execute operation
        cle_input1 = cle.push(input1.data)
        output = None
        operation = cle.operation(operation_name)
        # update GUI
        label_parameters(operation, [transform.a, transform.b, transform.c, transform.d, transform.e])
        output = _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output, a, b, c, d, e])
        output = cle.pull(output).astype(int)

        # show result in napari
        if not hasattr(transform.self, 'layer'):
            if isinstance(input1, Labels):
                transform.self.viewer.add_labels(output, translate=translate)
            else:
                transform.self.viewer.add_image(output, translate=translate)
        else:
            transform.self.layer.data = output
            transform.self.layer.contrast_limits = input1.contrast_limits
            transform.self.layer.name = "Result of " + operation.__name__
            transform.self.layer.translate = translate

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    input1={'label':'Image'},
    operation_name={'label': 'Operation', 'choices':cle.operations(must_have_categories=['projection', 'in assistant']).keys()}
)
def projection(input1: Layer, operation_name : str = cle.maximum_z_projection.__name__):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push(input1.data)
        output = None
        operation = cle.operation(operation_name)
        output = _call_operation_ignoring_to_many_arguments(operation, [cle_input1, output])
        output = cle.pull(output).astype(int)


        # show result in napari
        if not hasattr(projection.self, 'layer'):
            if isinstance(input1, Labels):
                projection.self.viewer.add_labels(output, translate=input1.translate[1:3])
            else:
                projection.self.viewer.add_image(output, translate=input1.translate[1:3])
        else:
            projection.self.layer.data = output
            projection.self.layer.contrast_limits = input1.contrast_limits
            projection.self.layer.name = "Result of " + operation.__name__
            projection.self.layer.translate = input1.translate[1:3]
