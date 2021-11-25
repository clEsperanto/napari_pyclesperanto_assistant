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
        # Read more: http://clesperanto.net
        #
        # To make this script run in Fiji, please activate the clij, clij2 and
        # clijx-assistant update sites in your Fiji.
        #
        # Read more: https://clij.github.io/
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
        if "imread" in step.operation:
            args = step.inputs
        else:
            inter = "labels_" if step.is_labels else ""
            args = step.inputs + [f"cle.create_{inter}like({step.inputs[0]})"] + step.args
        return f"{step.output} = cle.{step.operation}({', '.join(map(str, args))})"

    @staticmethod
    def show(step):
        title = f"Result of {step.operation.replace('_', ' ')}"
        show_args = [f"{step.output}", repr(title), str(step.is_labels)]
        if step.clims:
            show_args.extend(map(str, step.clims))
        return f"cle.imshow({', '.join(show_args)})"

    @staticmethod
    def newline():
        return ""

class NapariPythonGenerator(JythonGenerator):
    @staticmethod
    def header():
        from napari_pyclesperanto_assistant import __version__
        from textwrap import dedent

        return dedent(
            f"""
            # To make this script run in napari's script editor, install 
            # pyclesperanto_prototype and the script editor
            #
            # ```
            # pip install pyclesperanto_prototype napari-script-editor
            # ```
            # Read more: http://clesperanto.net
            #
            # Generator (P) version: {__version__}
            #
            
            import pyclesperanto_prototype as cle
            import napari

            if 'viewer' not in globals():
                viewer = napari.Viewer()
            """
        ).strip()

    @staticmethod
    def imports():
        return ""

    @staticmethod
    def subheader(step):
        if "imread" in step.operation:
            from textwrap import dedent

            return dedent(
                f"""
                # todo: configure which inputs should be taken here.
                # This takes the first selected layer's image data:
                """).strip()
        else:
            return JythonGenerator.subheader(step)

    @staticmethod
    def operate(step) -> str:
        from textwrap import dedent

        if "imread" in step.operation:
            return dedent(
                f"""
                {step.output} = cle.push(list(viewer.layers.selection)[0].data)
                """).strip()
        else:
            return JythonGenerator.operate(step)

    @staticmethod
    def show(step):
        if "imread" in step.operation:
            return ""

        code = ""
        name = f"Result of {step.operation.replace('_', ' ')}"
        if step.is_labels:
            code = code + "viewer.add_labels("
        else:
            code = code + "viewer.add_image("

        code = code + f"{step.output}"
        code = code + f", name='{name}'"
        if step.clims and not step.is_labels:
            code = code + ", contrast_limits=" + str(step.clims)
        code = code + ")"
        return code


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

    def to_napari_python(self, filename=None):
        code = "\n".join(self._generate(NapariPythonGenerator)).replace("\n\n\n\n", "\n\n")
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
            op, inputs, args, is_labels, min_intensity, max_intensity = graph[key]
            steps.append(Step(operation=op.__name__, inputs=inputs, args=args, output=key, is_labels=is_labels, clims=(min_intensity, max_intensity)))
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
