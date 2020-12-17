

class ScriptGenerator():
    def __init__(self, layers):
        self.layers = layers

    def _comment(self, text):
        return text

    def _finish(self, code : str):
        return code

    def file_ending(self):
        return ".txt"