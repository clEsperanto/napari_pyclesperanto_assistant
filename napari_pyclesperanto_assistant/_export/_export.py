from ._jython import JythonGenerator
from ._notebook import PythonJupyterNotebookGenerator
from pathlib import Path


def export_jython_code(layers, filename):
    generator = JythonGenerator(layers)
    code = generator.generate()
    if not filename.endswith(generator.file_ending()):
        filename += generator.file_ending()

    Path(filename).write_text(code)
    return filename


def export_jython_code_to_clipboard(layers):
    generator = JythonGenerator(layers)
    code = generator.generate()
    import pyperclip

    pyperclip.copy(code)


def export_notebook(self, layers, filename):
    generator = PythonJupyterNotebookGenerator(layers)
    code = generator.generate()

    if not filename.endswith(generator.file_ending()):
        filename += generator.file_ending()

    if filename is not None:
        Path(filename).write_text(code)
        import os

        # NOTE: probably better to use subprocess.run here?
        os.system("jupyter nbconvert --to notebook --inplace --execute " + filename)
        # os.system('jupyter notebook ' + filename) # todo: this line freezes napari

    return filename
