from typing import Any, Optional, Sequence, Tuple
from dataclasses import dataclass, field


@dataclass
class Step:
    operation: str
    args: Sequence[Any] = field(default_factory=tuple)  # kwargs might be better
    input: Optional[int] = None
    is_labels: bool = False
    clims: Optional[Tuple[float, float]] = None

    def operate(self, n) -> str:
        args = tuple(map(repr, self.args))
        if self.input:
            args = (f"image{n-1}", f"cle.create_like(image{n-1})") + args
        return f"image{n} = cle.{self.operation}({', '.join(map(str, args))})"

    def show(self, n):
        title = f"Result of {self.operation.replace('_', ' ')}"
        show_args = [f"image{n}", repr(title), str(self.is_labels)]
        if self.clims:
            show_args.extend(map(str, self.clims))
        return f"cle.imshow({', '.join(show_args)})"


@dataclass
class Pipeline:
    steps: Sequence[Step]
    show: bool = True

    def to_jython(self):
        for n, step in enumerate(self.steps):
            yield step.operate(n)
            if self.show:
                yield step.show(n)
            yield ""  # newline


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
