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
            f"""
        # To make this script run in cpython, install pyclesperanto_prototype:
        #
        # ```
        # pip install pyclesperanto_prototype
        # ```
        # Read more: https://clesperanto.net
        #
        # To make this script run in Fiji, please activate the clij, clij2 and
        # clijx-assistant update sites in your Fiji.
        #
        # Read more: https://clij.github.io/assistant
        #
        # Generator (P) version: {__version__}
        #
        """
        ).strip()

    @staticmethod
    def imports():
        return "import pyclesperanto_prototype as cle"

    @staticmethod
    def subheader(step):
        # jupytext will render "# ##" as an h2 header in ipynb
        return f"# ## {step.operation.replace('_', ' ')}"

    @staticmethod
    def operate(step) -> str:
        # TODO: in case of imread, we may do something special here...
        args = step.inputs + [f"cle.create_like({step.inputs[0]})"] + step.args
        return f"{step.output} = cle.{step.operation}({', '.join(map(str, args))})"

    @staticmethod
    def show(step):
        title = f"Result of {step.operation.replace('_', ' ')}"
        show_args = [f"image{n}", repr(title), str(step.is_labels)]
        if step.clims:
            show_args.extend(map(str, step.clims))
        return f"cle.imshow({', '.join(show_args)})"

    @staticmethod
    def newline():
        return ""


@dataclass
class Step:
    operation: str
    args: Sequence[Any] = field(default_factory=tuple)  # kwargs might be better
    inputs: Sequence[Any] = field(default_factory=tuple)
    output: str = "image"
    is_labels: bool = False
    clims: Optional[Tuple[float, float]] = None

@dataclass
class Pipeline:
    steps: Sequence[Step]
    show: bool = True

    def _generate(self, vistor):
        yield vistor.header()
        yield vistor.newline()
        yield vistor.imports()
        yield vistor.newline()
        yield vistor.newline()
        for step in self.steps:
            yield vistor.subheader(step)
            yield vistor.newline()
            yield vistor.operate(step)
            if self.show:
                yield vistor.show(step)
            yield vistor.newline()

    def to_jython(self, filename=None):
        code = "\n".join(self._generate(JythonGenerator))
        if filename:
            filename = Path(filename).expanduser().resolve()
            filename.write_text(code)
        return code

    def to_notebook(self, filename=None, execute=False):
        import jupytext

        # jython code is created in the jupytext light format
        # https://jupytext.readthedocs.io/en/latest/formats.html#the-light-format

        jt = jupytext.reads(self.to_jython(), fmt="py:light")
        nb = jupytext.writes(jt, fmt="ipynb")
        if filename:
            filename = Path(filename).expanduser().resolve()
            filename.write_text(nb)
            # could use a NamedTemporaryFile to run this even without write
            if execute:
                from subprocess import Popen
                from shutil import which

                if not which("jupyter-notebook"):
                    raise RuntimeError("Cannot find jupyter-notebook executable")

                try:
                    Popen(["jupyter-notebook", "-y", str(filename)])
                except Exception as e:
                    warnings.warn(f"Failed to execute notebook: {e}")
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
        for key in dask.order.order(graph):
            op, inputs, args = graph[key]
            steps.append(Step(operation=op.__name__, inputs=inputs, args=args, output=key))
        return cls(steps=steps)


if __name__ == "__main__":
    lund = Path(__file__).parent / "data" / "Lund_000500_resampled-cropped.tif"
    s0 = Step(operation="imread", args=(str(lund.resolve()),), clims=(125, 680))
    s1 = Step(operation="gaussian_blur", input=s0, args=(1, 1, 0), clims=(0, 657))
    s2 = Step(operation="top_hat_box", input=s1, args=(10, 10, 0), clims=(0, 378))
    s3 = Step(operation="gamma_correction", input=s2, args=(1,), clims=(0, 378))
    s4 = Step(operation="threshold_otsu", input=s3, is_labels=True)
    s5 = Step(operation="connected_components_labeling_box", input=s3, is_labels=True)

    Pipeline(steps=[s0, s1, s2, s3, s4, s5]).to_notebook("~/Desktop/test.ipynb", True)
