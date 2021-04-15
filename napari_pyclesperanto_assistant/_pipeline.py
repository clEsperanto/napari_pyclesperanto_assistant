import warnings
from typing import Any, Optional, Sequence, Tuple
from dataclasses import dataclass, field
from pathlib import Path


class JythonGenerator:
    @staticmethod
    def header():
        from napari_pyclesperanto_assistant import __version__
        from textwrap import dedent

        return dedent(
            f'''
        """
        To make this script run in cpython, install pyclesperanto_prototype:
        pip install pyclesperanto_prototype
        Read more: https://clesperanto.net

        To make this script run in Fiji, please activate the clij,
        clij2 and clijx-assistant update sites in your Fiji.

        Read more: https://clij.github.io/assistant
        Generator (P) version: {__version__}
        """

        '''
        )

    @staticmethod
    def imports():
        return "import pyclesperanto_prototype as cle"

    @staticmethod
    def subheader(step, n):
        return f"\n# {step.operation}"

    @staticmethod
    def operate(step, n) -> str:
        args = step.args
        from napari_pyclesperanto_assistant._gui._category_widget import OUTPUT_PLACEHOLDER
        args = [f"cle.create_like({step.args[0]})" if x == OUTPUT_PLACEHOLDER else x for x in args]

        return f"{step.output} = cle.{step.operation}({', '.join(map(str, args))})"

    @staticmethod
    def show(step, n):
        title = f"Result of {step.operation.replace('_', ' ')}"
        show_args = [f"image{n}", repr(title), str(step.is_labels)]
        if step.clims:
            show_args.extend(map(str, step.clims))
        return f"cle.imshow({', '.join(show_args)})"

from nbformat.v4 import new_code_cell
from nbformat.v4 import new_markdown_cell
class NotebookGenerator:
    @staticmethod
    def header():
        return new_markdown_cell(JythonGenerator.header())

    @staticmethod
    def imports():
        return new_code_cell(JythonGenerator.imports())

    @staticmethod
    def subheader(step, n):
        return new_markdown_cell(JythonGenerator.subheader(step, n))

    @staticmethod
    def operate(step, n) -> str:
        return new_code_cell(JythonGenerator.operate(step, n))

    @staticmethod
    def show(step, n):
        return new_code_cell(JythonGenerator.show(step, n))


@dataclass
class Step:
    operation: str
    args: Sequence[Any] = field(default_factory=tuple)  # kwargs might be better
    output: str = "image"
    is_labels: bool = False
    clims: Optional[Tuple[float, float]] = None

@dataclass
class Pipeline:
    steps: Sequence[Step]
    show: bool = True

    def _generate(self, vistor):
        yield vistor.header()
        yield vistor.imports()
        for n, step in enumerate(self.steps):
            yield vistor.subheader(step, n)
            yield vistor.operate(step, n)
            if self.show:
                yield vistor.show(step, n)

    def to_jython(self, filename=None):
        code = "\n".join(self._generate(JythonGenerator))
        if filename:
            Path(filename).write_text(code)
        return code

    def to_notebook(self, filename=None):
        # Todo: I assume there is a better way of doing the following 3 lines
        cells = []
        for i in self._generate(NotebookGenerator):
            cells.append(i)

        # build notebook
        from nbformat import NotebookNode
        nb = NotebookNode()
        nb["cells"] = cells
        nb["metadata"] = {}
        nb["nbformat"] = 4
        nb["nbformat_minor"] = 5

        if filename:
            # write notebook to disc
            from nbformat import write
            write(nb, filename)

            # Execute notebook
            from nbconvert.preprocessors import ExecutePreprocessor
            from nbclient.exceptions import CellExecutionError
            ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
            try:
                ep.preprocess(nb, {"metadata": {"path": "."}})
            except CellExecutionError:
                warnings.warn("Notebook execution failed. See the notebook file for details.")
                return

            # write executed notebook to disc
            write(nb, filename)

        return nb

    def __str__(self):
        return self.to_jython()

    @classmethod
    def from_assistant(cls, asst):
        return cls.from_dask(asst.to_dask())

    @classmethod
    def from_dask(cls, graph):
        import dask
        steps = []
        for key in graph.keys(): # Robert observed that this didn't work: dask.order.order(graph):
            op, *args = graph[key]
            steps.append(Step(operation=op.__name__, args=args, output=key))
        return cls(steps=steps)


if __name__ == "__main__":
    s0 = Step(operation="imread", args=("Lund_000500",), clims=(125, 680))
    s1 = Step(operation="gaussian_blur", input=s0, args=(1, 1, 0), clims=(0, 657))
    s2 = Step(operation="top_hat_box", input=s1, args=(10, 10, 0), clims=(0, 378))
    s3 = Step(operation="gamma_correction", input=s2, args=(1,), clims=(0, 378))
    s4 = Step(operation="threshold_otsu", input=s3, is_labels=True)
    s5 = Step(
        operation="connected_components_labeling_box",
        input=s3,
        args=(2,),
        is_labels=True,
    )

    print(Pipeline(steps=[s0, s1, s2, s3, s4, s5]))
