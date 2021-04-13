from napari.layers import Image, Labels
import pyclesperanto_prototype as cle

from ._base_generator import ScriptGenerator


class JythonGenerator(ScriptGenerator):
    def _header(self):
        from .. import __version__ as version

        return (
            "# To make this script run in cpython, install pyclesperanto_prototype:\n"
            + "# pip install pyclesperanto_prototype\n"
            + "# Read more: \n"
            + "# https://clesperanto.net\n"
            + "# \n"
            + "# To make this script run in Fiji, please activate the clij, \n"
            + "# clij2 and clijx-assistant update sites in your Fiji. \n"
            + "# Read more: \n"
            + "# https://clij.github.io/assistant\n"
            + "# \n"
            + "# Generator (P) version: "
            + version
            + "\n"
            + "# \n"
            + "import pyclesperanto_prototype as cle\n\n"
        )

    def _push(self, layer, layer_number):

        if "filename" in layer.metadata:
            import os

            filename = layer.metadata["filename"]
            filename = os.path.abspath(filename)
            # windows path fix
            filename = filename.replace("\\", "/")
        else:
            filename = layer.name

        return "image" + str(layer_number) + " = cle.imread('" + filename + "')\n"

    def _execute(self, layer, layer_number):
        command = ""
        try:
            method = cle.operation(
                layer.metadata["dialog"].filter_gui.operation_name.value
            )
            parameter_names = method.fullargspec.args
            method_name = "cle." + method.__name__
            method_name = method_name.replace("please_select", "copy")
        except AttributeError:
            method = layer.metadata["dialog"].filter_gui._function

            # let's chat about this, probably a better way
            import inspect

            parameter_names = inspect.getfullargspec(method).args
            method_name = method.__name__

            command = (
                command
                + "from "
                + method.__module__
                + " import "
                + method.__qualname__
                + "\n"
            )

        command = command + method_name + "("

        first_image_parameter = None

        put_comma = False
        for i, parameter_name in enumerate(
            [x.name for x in layer.metadata["dialog"].filter_gui]
        ):
            if i < len(parameter_names):
                comma = ""
                if put_comma:
                    comma = ", "
                put_comma = True

                widget = layer.metadata["dialog"].filter_gui[parameter_name]

                value = widget.value

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

        if first_image_parameter is not None:
            command = (
                "image"
                + str(layer_number)
                + " = cle.create_like("
                + first_image_parameter
                + ")\n"
                + "image"
                + str(layer_number)
                + " = "
                + command
            )

        command = "\n" + self._comment(" Layer " + layer.name) + "\n" + command

        return command

    def _pull(self, layer, layer_number):

        if isinstance(layer, Labels):
            is_labels = "True"
            intensity_config = ""

        else:
            is_labels = "False"
            intensity_config = (
                ", "
                + str(layer.contrast_limits[0])
                + ", "
                + str(layer.contrast_limits[1])
            )

        what_to_show = "image" + str(layer_number)

        code = (
            self._comment(" show result")
            + "\n"
            + "cle.imshow("
            + what_to_show
            + ", '"
            + layer.name
            + "', "
            + is_labels
            + intensity_config
            + ")\n"
        )

        return code

    def _get_index_of_layer(self, layer):
        for i, other_layer in enumerate(self.layers):
            if other_layer == layer:
                return i

    def _comment(self, text):
        return "#" + text

    def file_ending(self):
        return ".py"