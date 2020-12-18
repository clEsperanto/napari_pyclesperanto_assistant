from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox
from magicgui._qt.widgets import QDataComboBox
from napari.layers import Image, Labels
import pyclesperanto_prototype as cle

from ._ScriptGeneratorBase import ScriptGenerator

class JythonGenerator(ScriptGenerator):

    def _header(self):
        return "import net.clesperanto.javaprototype.Snake as cle\n"

    def _push(self, layer, layer_number):
        return "from ij import IJ\n" + \
            "image = IJ.openImage('" + layer.filename.replace("\\", "/") + "')\n" + \
            "image" + str(layer_number) + " = cle.push(image)\n" + \
            "image.show()\n"

    def _execute(self, layer, layer_number):
        method = cle.operation(layer.dialog.filter_gui.get_widget("operation_name").currentData())
        method_name = method.__name__
        method_name = "cle." + method_name
        method_name = method_name.replace("please_select", "copy")
        command = method_name + "("

        parameter_names = method.fullargspec.args

        first_image_parameter = None

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
        command = "image" + str(layer_number) + " = cle.create(" + first_image_parameter + ")\n" + \
                                                command

        command = self._comment(" Layer " + layer.name) + "\n" + command
        if (layer.visible):
            command = command + self._pull(layer, layer_number)
        return command


    def _pull(self, layer, layer_number):
        code = self._comment(" show result") + "\n" + \
               "image = cle.pull(image" + str(layer_number) + ")\n" + \
               "image.setTitle(\"" + layer.name + "\")\n"
        if isinstance(layer, Labels):
            code = code + \
                "image.resetDisplayRange()\n" + \
                "IJ.run(image, \"glasbey_on_dark\", \"\")\n"
        else:
            code = code + \
                "image.setDisplayRange(" + str(layer.contrast_limits[0]) + ", " + str(layer.contrast_limits[1]) + ")\n"

        code = code + \
               "image.show()\n"
        return code

    def _get_index_of_layer(self, layer):
        for i, other_layer in enumerate(self.layers):
            if other_layer == layer:
                return i

    def _export_layer(self, layer, layer_number):
        code = ""

        record_push = False
        try:
            if layer.filename is not None:
                record_push = True
        except:
            pass
        if record_push:
            code = code + self._push(layer, layer_number)

        record_exec = False
        try:
            if layer.dialog is not None:
                record_exec = True
        except:
            pass
        if record_exec:
            code = code + self._execute(layer, layer_number)

        for i, other_layer in enumerate(self.layers):
            parse_layer = False
            try:
                if other_layer.dialog is not None:
                    if (other_layer.dialog.filter_gui.get_widget("input1").currentData() == layer):
                        parse_layer = True
                    if (other_layer.dialog.filter_gui.get_widget("input2").currentData() == layer):
                        parse_layer = True
            except AttributeError:
                pass
            if parse_layer:
                code = code + self._export_layer(other_layer, i)
        return code

    def _comment(self, text):
        return "#" + text


    def file_ending(self):
        return ".py"