from ._jython import JythonGenerator


class PythonJupyterNotebookGenerator(JythonGenerator):
    def _header(self):
        return "{\n" + ' "cells": [\n' + self._code_cell(super()._header())

    def _push(self, layer, layer_number):
        return self._code_cell(super()._push(layer, layer_number))

    def _execute(self, layer, layer_number):
        return self._markdown_cell(
            "## " + layer.name.replace("Result of ", "")
        ) + self._code_cell(super()._execute(layer, layer_number))

    def _pull(self, layer, layer_number):
        return self._code_cell(super()._pull(layer, layer_number))

    def _code_cell(self, content):
        return (
            "  {\n"
            + '   "cell_type": "code",\n'
            + '   "execution_count": 1,\n'
            + '   "metadata": {},\n'
            + '   "outputs": [],\n'
            + '   "source": [\n'
            + '    "'
            + content.replace('"', "'").replace("\n", '\\n",\n"')
            + '"\n'
            + "   ]\n"
            + "  },"
        )

    def _markdown_cell(self, content):
        return (
            "  {\n"
            + '   "cell_type": "markdown",\n'
            + '   "metadata": {},\n'
            + '   "source": [\n'
            + '    "'
            + content.replace("\n", '\\n",\n"')
            + '"\n'
            + "   ]\n"
            + "  },"
        )

    def _finish(self, code: str):
        return (
            super()._finish(code[0:-1])
            + ""
            + "],\n"
            + ' "metadata": {\n'
            + '  "kernelspec": {\n'
            + '   "display_name": "Python 3",\n'
            + '   "language": "python",\n'
            + '   "name": "python3"\n'
            + "  },\n"
            + '  "language_info": {\n'
            + '   "codemirror_mode": {\n'
            + '    "name": "ipython",\n'
            + '    "version": 3\n'
            + "   },\n"
            + '   "file_extension": ".py",\n'
            + '   "mimetype": "text/x-python",\n'
            + '   "name": "python",\n'
            + '   "nbconvert_exporter": "python",\n'
            + '   "pygments_lexer": "ipython3",\n'
            + '   "version": "3.7.6"\n'
            + "  }\n"
            + " },\n"
            + ' "nbformat": 4,\n'
            + ' "nbformat_minor": 4\n'
            + "}\n"
        )

    def file_ending(self):
        return ".ipynb"