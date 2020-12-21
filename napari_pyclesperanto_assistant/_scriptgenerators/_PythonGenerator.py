from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox
from magicgui._qt.widgets import QDataComboBox
from napari.layers import Image, Labels
import pyclesperanto_prototype as cle

from ._ScriptGeneratorBase import ScriptGenerator

class PythonGenerator(ScriptGenerator):

    def _header(self):
        from .. import __version__ as version

        return "# To make this script run in cpython, install pyclesperanto_prototype:\n" + \
                "# pip install pyclesperanto_prototype\n" + \
                "# Read more: \n" + \
                "# https://clesperanto.net\n" + \
                "# \n" + \
                "# Generator (P) version: " + version + "\n" + \
                "# \n" + \
                "import pyclesperanto_prototype as cle\n" + \
                "from skimage.io import imread, imshow\n\n"

    def _push(self, layer, layer_number):

        if hasattr(layer, "filename"):
            filename = layer.filename.replace("\\", "/")
        else:
            filename = layer.name

        return \
            "image = imread('" + filename + "')\n" + \
            "image" + str(layer_number) + " = cle.push_zyx(image)\n"

    def _execute(self, layer, layer_number):
        method = cle.operation(layer.dialog.filter_gui.get_widget("operation_name").currentData())
        method_name = method.__name__
        method_name = "cle." + method_name
        method_name = method_name.replace("please_select", "copy")
        command = method_name + "("

        parameter_names = method.fullargspec.args

        put_comma = False
        for i, parameter_name in enumerate(layer.dialog.filter_gui.param_names):
            if (i < len(parameter_names)):
                comma = ""
                if put_comma:
                    comma = ", "
                put_comma = True

                widget = layer.dialog.filter_gui.get_widget(parameter_name)

                if isinstance(widget, QDoubleSpinBox) or isinstance(widget, QSpinBox):
                    value = widget.value()
                elif isinstance(widget, QDataComboBox):
                    value = widget.currentData()
                else:
                    value = None

                if value == method: # operation
                    pass
                elif isinstance(value, Image) or isinstance(value, Labels):
                    command = command + comma + parameter_names[i] + "=image" + str(self._get_index_of_layer(value))
                elif isinstance(value, str):
                    if parameter_name != "operation_name":
                        command = command + comma + parameter_names[i] + "='" + value + "'"
                else:
                    command = command + comma + parameter_names[i] + "=" + str(value)

        command = command + ")\n"
        command = "image" + str(layer_number) + " = " + command

        command = self._comment(" Layer " + layer.name) + "\n" + command
        return command

    def _pull(self, layer, layer_number):
        return self._comment(" show result") + "\n" + \
        "imshow(cle.pull_zyx(image" + str(layer_number) + "))\n\n"

    def _get_index_of_layer(self, layer):
        for i, other_layer in enumerate(self.layers):
            if other_layer == layer:
                return i

    def _comment(self, text):
        return "#" + text


    def file_ending(self):
        return ".py"