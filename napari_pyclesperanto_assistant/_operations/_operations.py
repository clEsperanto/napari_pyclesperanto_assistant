
# -----------------------------------------------------------------------------
# The user interface of the _operations is build by magicgui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from magicgui import magicgui
from napari.layers import Image
import pyclesperanto_prototype as cle

@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['filter', 'denoise','in assistant'], must_not_have_categories=['combine']).keys()},
    x={'minimum': -1000, 'maximum': 1000},
    y={'minimum': -1000, 'maximum': 1000},
    z={'minimum': -1000, 'maximum': 1000},
)
def denoise(input1: Image, operation_name: str = cle.gaussian_blur.__name__, x: float = 1, y: float = 1, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        operation(cle_input, output, x, y, z)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (denoise.initial_call):
            denoise.self.viewer.add_image(output, colormap=input1.colormap)
            denoise.initial_call = False
        else:
            denoise.self.layer.data = output
            denoise.self.layer.name = operation.__name__
            denoise.self.layer.contrast_limits=(0, max_intensity)

@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['filter', 'background removal','in assistant'], must_not_have_categories=['combine']).keys()},
    x={'minimum': -1000, 'maximum': 1000},
    y={'minimum': -1000, 'maximum': 1000},
    z={'minimum': -1000, 'maximum': 1000},
)
def background_removal(input1: Image, operation_name: str = cle.top_hat_box.__name__, x: float = 10, y: float = 10, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        operation(cle_input, output, x, y, z)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (background_removal.initial_call):
            background_removal.self.viewer.add_image(output, colormap=input1.colormap)
            background_removal.initial_call = False
        else:
            background_removal.self.layer.data = output
            background_removal.self.layer.name = operation.__name__
            background_removal.self.layer.contrast_limits=(0, max_intensity)

@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['filter', 'in assistant'], must_not_have_categories=['combine', 'denoise', 'background removal']).keys()},
    x={'minimum': -1000, 'maximum': 1000},
    y={'minimum': -1000, 'maximum': 1000},
    z={'minimum': -1000, 'maximum': 1000},
)
def filter(input1: Image, operation_name: str = cle.gamma_correction.__name__, x: float = 1, y: float = 1, z: float = 0):
    if input1:
        # execute operation
        cle_input = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input)
        operation = cle.operation(operation_name)
        operation(cle_input, output, x, y, z)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (filter.initial_call):
            filter.self.viewer.add_image(output, colormap=input1.colormap)
            filter.initial_call = False
        else:
            filter.self.layer.data = output
            filter.self.layer.name = operation.__name__
            filter.self.layer.contrast_limits=(0, max_intensity)

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['binarize', 'in assistant'], must_not_have_categories=['combine']).keys()},
    constant={'minimum':-1000, 'maximum':1000}
)
def binarize(input1: Image, operation_name : str = cle.threshold_otsu.__name__, constant : int = 0):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, output, constant)
        output = cle.pull_zyx(output)

        # show result in napari
        if (binarize.initial_call):
            binarize.self.viewer.add_image(output)
            binarize.initial_call = False
        else:
            binarize.self.layer.data = output
            binarize.self.layer.contrast_limits = (0, 1)
            binarize.self.layer.name = operation.__name__

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['combine', 'in assistant']).keys()}
)
def combine(input1: Image, input2: Image = None, operation_name: str = cle.binary_and.__name__):
    if input1 is not None:
        if (input2 is None):
            input2 = input1

        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        cle_input2 = cle.push_zyx(input2.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, cle_input2, output)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (combine.initial_call):
            combine.self.viewer.add_image(output, colormap=input1.colormap)
            combine.initial_call = False
        else:
            combine.self.layer.data = output
            combine.self.layer.name = operation.__name__
            combine.self.layer.contrast_limits=(0, max_intensity)

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['label', 'in assistant']).keys()}
)
def label(input1: Image, operation_name: str = cle.connected_components_labeling_box.__name__):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, output)
        output = cle.pull_zyx(output)

        # show result in napari
        if (label.initial_call):
            label.self.viewer.add_labels(output)
            label.initial_call = False
        else:
            label.self.layer.data = output
            label.self.layer.name = operation.__name__

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['label processing', 'in assistant']).keys()},
    min = {'minimum': -1000, 'maximum': 1000},
    max = {'minimum': -1000, 'maximum': 1000}
)
def label_processing(input1: Image, operation_name: str = cle.exclude_labels_on_edges.__name__, min: float=0, max:float=100):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, output, min, max)
        output = cle.pull_zyx(output)

        # show result in napari
        if (label_processing.initial_call):
            label_processing.self.viewer.add_labels(output)
            label_processing.initial_call = False
        else:
            label_processing.self.layer.data = output
            label_processing.self.layer.name = operation.__name__

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['label measurement', 'mesh', 'in assistant'], must_not_have_categories=["combine"]).keys()},
    n = {'minimum': 0, 'maximum': 1000}
)
def mesh(input1: Image, operation_name : str = cle.draw_mesh_between_touching_labels.__name__, n : float = 1):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, output, n)
        min_intensity = cle.minimum_of_all_pixels(output)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity - min_intensity == 0:
            max_intensity = min_intensity + 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (mesh.initial_call):
            mesh.self.viewer.add_image(output, colormap='green', blending='additive')
            mesh.initial_call = False
        else:
            mesh.self.layer.data = output
            mesh.self.layer.name = operation.__name__
            mesh.self.layer.contrast_limits=(min_intensity, max_intensity)

# -----------------------------------------------------------------------------
@magicgui(
    auto_call=True,
    layout='vertical',
    operation_name={'choices':cle.operations(must_have_categories=['label measurement', 'map', 'in assistant'], must_not_have_categories=["combine"]).keys()},
    n = {'minimum': 0, 'maximum': 1000}
)
def map(input1: Image, operation_name: str = cle.label_pixel_count_map.__name__, n : float = 1):
    if input1 is not None:
        # execute operation
        cle_input1 = cle.push_zyx(input1.data)
        output = cle.create_like(cle_input1)
        operation = cle.operation(operation_name)
        operation(cle_input1, output, n)
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (map.initial_call):
            map.self.viewer.add_image(output, colormap='magenta')
            map.initial_call = False
        else:
            map.self.layer.data = output
            map.self.layer.name = operation.__name__
            map.self.layer.contrast_limits=(0, max_intensity)

# -----------------------------------------------------------------------------
# A special case of ooperation is measurement: it results in a table instead of
# an image
@magicgui(layout='vertical', call_button="Measure")
def measure(input1: Image = None, labels : Image = None):
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
