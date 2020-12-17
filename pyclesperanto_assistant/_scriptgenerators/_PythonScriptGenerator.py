from ._ScriptGeneratorBase import ScriptGenerator

class PythonScriptGenerator(ScriptGenerator):
    def __init__(self, layers):
        self.layers = layers
    def generate(self):
        code = self._header()

        for i, layer in enumerate(self.layers):
            parse_layer = False
            try:
                layer.dialog
            except AttributeError:
                parse_layer = True
            if parse_layer:
                code = code + self._export_layer(layer, i)

        code = code + "\n" + self._comment(" show result") + "\n" \
                      "from skimage.io import imshow\n" + \
            "imshow(cle.pull_zyx(image" + str(len(self.layers) - 1) + "))\n"

        return code

    def _header(self):
        return "import pyclesperanto_prototype as cle\n"

    def _push(self, layer, layer_number):
        return "from skimage.io import imread\n" + \
            "image = imread('" + layer.filename + "')\n" + \
            "image" + str(layer_number) + " = cle.push_zyx(image)\n"

    def _execute(self, layer, layer_number):
        method = cle.operation(cle.operation(layer.dialog.filter_gui.get_widget("operation").currentData()))
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
                    command = command + comma + parameter_names[i] + "='" + value + "'"
                else:
                    command = command + comma + parameter_names[i] + "=" + str(value)

        command = command + ")\n"
        command = "image" + str(layer_number) + " = " + command

        return command

    def _get_index_of_layer(self, layer):
        for i, other_layer in enumerate(self.layers):
            if other_layer == layer:
                return i

    def _export_layer(self, layer, layer_number):
        code = "\n" + self._comment(" Layer " + layer.name) + "\n"

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
