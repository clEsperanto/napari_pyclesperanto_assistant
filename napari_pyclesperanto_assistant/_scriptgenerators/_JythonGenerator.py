from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox
from magicgui._qt.widgets import QDataComboBox
from napari.layers import Image, Labels
import pyclesperanto_prototype as cle

from ._ScriptGeneratorBase import ScriptGenerator

class JythonGenerator(ScriptGenerator):

    def _header(self):
        from .. import __version__ as version

        return \
        "# To make this script run in cpython, install pyclesperanto_prototype:\n" + \
        "# pip install pyclesperanto_prototype\n" + \
        "# Read more: \n" + \
        "# https://clesperanto.net\n" + \
        "# \n" + \
        "# To make this script run in Fiji, please activate the clij, \n" + \
        "# clij2 and clijx-assistant update sites in your Fiji. \n" + \
        "# Read more: \n" + \
        "# https://clij.github.io/assistant\n" + \
        "# \n" + \
        "# Generator (P) version: " + version + "\n" + \
        "# \n" + \
        "import pyclesperanto_prototype as cle\n\n"

    def _push(self, layer, layer_number):

        if 'filename' in layer.metadata:
            filename = layer.metadata['filename'].replace("\\", "/")
        else:
            filename = layer.name

        return "image" + str(layer_number) + " = cle.imread('" + filename + "')\n"


    def _execute(self, layer, layer_number):
        method = cle.operation(layer.metadata['dialog'].filter_gui.get_widget("operation_name").currentData())
        method_name = method.__name__
        method_name = "cle." + method_name
        method_name = method_name.replace("please_select", "copy")
        command = "image" + str(layer_number) + " = " + method_name + "("

        parameter_names = method.fullargspec.args

        first_image_parameter = None

        put_comma = False
        for i, parameter_name in enumerate(layer.metadata['dialog'].filter_gui.param_names):
            if (i < len(parameter_names)):
                comma = ""
                if put_comma:
                    comma = ", "
                put_comma = True

                widget = layer.metadata['dialog'].filter_gui.get_widget(parameter_name)

                if isinstance(widget, QDoubleSpinBox) or isinstance(widget, QSpinBox):
                    value = widget.value()
                elif isinstance(widget, QDataComboBox):
                    value = widget.currentData()
                else:
                    value = None

                if isinstance(value, Image) or isinstance(value, Labels):
                    image_str = "image" + str(self._get_index_of_layer(value))
                    if first_image_parameter is None:
                        first_image_parameter = image_str
                    command = command + comma + image_str
                elif isinstance(value, str):
                    if parameter_name != "operation_name":
                        command = command + comma + "'" + value + "'"
                    else:
                        command = command + comma + "image" + str(layer_number)
                else:
                    command = command + comma + str(value)

        command = command + ")\n"
        command = "image" + str(layer_number) + " = cle.create_like(" + first_image_parameter + ")\n" + \
                                                command

        command = self._comment(" Layer " + layer.name) + "\n" + command

        return command


    def _pull(self, layer, layer_number):

        if isinstance(layer, Labels):
            is_labels = "True"
            intensity_config = ""

        else:
            is_labels = "False"
            intensity_config = ", " + str(layer.contrast_limits[0]) + ", " + str(layer.contrast_limits[1])

        what_to_show = "image" + str(layer_number)
        if len(layer.data.shape) > 2:
            what_to_show = "cle.maximum_z_projection(" + what_to_show + ")"

        code = self._comment(" show result") + "\n" + \
               "cle.imshow(" + what_to_show + ", '" + layer.name + "', " + is_labels + intensity_config + ")\n\n"

        return code

    def _get_index_of_layer(self, layer):
        for i, other_layer in enumerate(self.layers):
            if other_layer == layer:
                return i

    def _comment(self, text):
        return "#" + text


    def file_ending(self):
        return ".py"