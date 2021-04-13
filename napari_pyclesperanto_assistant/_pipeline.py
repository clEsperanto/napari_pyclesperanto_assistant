from typing import Any, Optional, Sequence, Tuple
from dataclasses import dataclass, field
from pathlib import Path


class JythonGenerator:
    @staticmethod
    def operate(step, n) -> str:
        args = tuple(map(repr, step.args))
        if step.input:
            args = (f"image{n-1}", f"cle.create_like(image{n-1})") + args
        return f"image{n} = cle.{step.operation}({', '.join(map(str, args))})"

    @staticmethod
    def show(step, n):
        title = f"Result of {step.operation.replace('_', ' ')}"
        show_args = [f"image{n}", repr(title), str(step.is_labels)]
        if step.clims:
            show_args.extend(map(str, step.clims))
        return f"cle.imshow({', '.join(show_args)})"


@dataclass
class Step:
    operation: str
    args: Sequence[Any] = field(default_factory=tuple)  # kwargs might be better
    input: Optional[int] = None
    is_labels: bool = False
    clims: Optional[Tuple[float, float]] = None


@dataclass
class Pipeline:
    steps: Sequence[Step]
    show: bool = True

    def _generate(self, vistor):
        for n, step in enumerate(self.steps):
            yield vistor.operate(step, n)
            if self.show:
                yield vistor.show(step, n)
            yield ""  # newline

    def to_jython(self, filename=None):
        code = "\n".join(self._generate(JythonGenerator))
        if filename:
            Path(filename).write_text()
        return code

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
            op, *args = graph[key]
            input = None
            for i, a in enumerate(args):
                if a in graph:
                    input = args.pop(i)
            steps.append(Step(operation=op.__name__, input=input, args=args))
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

    pipeline = Pipeline(steps=[s0, s1, s2, s3, s4, s5])

    print("\n".join(pipeline.to_jython()))
