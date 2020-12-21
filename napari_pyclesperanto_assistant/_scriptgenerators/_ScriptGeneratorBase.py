

class ScriptGenerator():
    def __init__(self, layers):
        self.layers = layers

    def generate(self):
        code = self._header()

        # search for entry point and generate code from there recusively
        for i, layer in enumerate(self.layers):
            if 'dialog' not in layer.metadata:
                code = code + self._export_layer(layer, i)
                break


        #code = code + self._pull(self.layers[-1], len(self.layers) - 1)

        return self._finish(code)

    def _export_layer(self, layer, layer_number):
        code = ""

        if hasattr(layer, 'metadata') and 'dialog' in layer.metadata:
            code = code + self._execute(layer, layer_number)
        else:
            code = code + self._push(layer, layer_number)


        if (layer.visible):
            code = code + self._pull(layer, layer_number)

        for i, other_layer in enumerate(self.layers):
            parse_layer = False
            try:
                if 'dialog' in other_layer.metadata:
                    if (other_layer.metadata['dialog'].filter_gui.get_widget("input1").currentData() == layer):
                        parse_layer = True
                    if (other_layer.metadata['dialog'].filter_gui.get_widget("input2").currentData() == layer):
                        parse_layer = True
            except AttributeError:
                pass
            if parse_layer:
                code = code + self._export_layer(other_layer, i)

        return code

    def _comment(self, text):
        return text

    def _finish(self, code : str):
        return code

    def file_ending(self):
        return ".txt"