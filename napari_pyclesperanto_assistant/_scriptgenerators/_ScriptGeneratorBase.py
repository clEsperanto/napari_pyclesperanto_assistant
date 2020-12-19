

class ScriptGenerator():
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

        #code = code + self._pull(self.layers[-1], len(self.layers) - 1)

        return self._finish(code)

    def _comment(self, text):
        return text

    def _finish(self, code : str):
        return code

    def file_ending(self):
        return ".txt"