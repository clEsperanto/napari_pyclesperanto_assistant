

class ScriptGenerator():
    def __init__(self, layers):
        self.layers = layers

    def generate(self):
        code = self._header()

        # search for entry point and generate code from there recusively
        for i, layer in enumerate(self.layers):
            code = code + self._export_layer(layer, i)

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

        return code

    def _comment(self, text):
        return text

    def _finish(self, code : str):
        return code

    def file_ending(self):
        return ".txt"