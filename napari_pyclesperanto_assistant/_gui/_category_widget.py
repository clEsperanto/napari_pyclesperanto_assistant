from __future__ import annotations

from inspect import Parameter, Signature, signature
from typing import TYPE_CHECKING, Sequence, Tuple

import pyclesperanto_prototype as cle
from loguru import logger
from magicgui import magicgui
from typing_extensions import Annotated

from .._categories import Category

if TYPE_CHECKING:
    from napari.layers import Layer

VIEWER_PARAM = "viewer"
OP_NAME_PARAM = "op_name"
OP_ID = "op_id"


def num_positional_args(func, types=[cle.Image, int, str, float, bool]) -> int:
    params = signature(func).parameters
    return len([p for p in params.values() if p.annotation in types])


@logger.catch
def call_op(
    op_name: str, inputs: Sequence[Layer], *args
) -> Tuple[cle.Image, Tuple[float, float]]:
    if not inputs or inputs[0] is None:
        return
    # transfer to gpu
    i0 = inputs[0].data
    gpu_ins = [cle.push(i.data if i is not None else i0) for i in inputs]
    gpu_out = cle.create_like(gpu_ins[0])
    # get cle function
    cle_function = cle.operation(op_name)  # couldn't this just be getattr(cle, ...)?
    # call function ignoring extra positional args
    nargs = num_positional_args(cle_function)
    logger.info(f"cle.{op_name}(..., {', '.join(map(str, args))})")
    args = ((*gpu_ins, gpu_out) + args)[:nargs]
    cle_function(*args)
    # return output
    return gpu_out


def _show_result(
    gpu_out, viewer, name: str, layer_type: str, op_id: int, translate=None, cmap=None
):
    if not viewer:
        print("NO VIEWER")
        return
    # show result in napari
    clims = [cle.minimum_of_all_pixels(gpu_out), cle.maximum_of_all_pixels(gpu_out)]

    if clims[1] == 0:
        clims[1] = 1

    data = cle.pull(gpu_out)
    if layer_type == "labels":
        data = data.astype(int)
    try:
        layer = next(x for x in viewer.layers if x.metadata.get(OP_ID) == op_id)
        logger.debug(f"updating existing layer: {layer}, with id: {op_id}")
        layer.data = data
        layer.name = name
        layer.contrast_limits = clims
        # layer.translate = translate
    except StopIteration:
        logger.debug(f"creating new layer for id: {op_id}")
        add_layer = getattr(viewer, f"add_{layer_type}")
        kwargs = dict(name=name, metadata={OP_ID: op_id})
        if layer_type == "image":
            kwargs["colormap"] = cmap
        layer = add_layer(data, **kwargs)
    return layer


def make_gui_for_category(category: Category) -> magicgui.widgets.FunctionGui:

    k = Parameter.KEYWORD_ONLY

    # add inputs
    params = []
    for n, t in enumerate(category.inputs):
        params.append(Parameter(name=f"input{n}", kind=k, annotation=t))

    # get valid operations choices
    choices = list(cle.operations(category.include, category.exclude))
    op_type = Annotated[str, {"choices": choices, "label": "Operation"}]
    params.append(
        Parameter(
            name=OP_NAME_PARAM, kind=k, annotation=op_type, default=category.default_op
        )
    )

    # add args
    for name, type_, default in category.args:
        params.append(Parameter(name=name, kind=k, annotation=type_, default=default))

    # add a viewer
    params.append(
        Parameter(
            name=VIEWER_PARAM, kind=k, annotation="napari.viewer.Viewer", default=None
        )
    )

    def gui_function(**kwargs):
        viewer = kwargs.pop(VIEWER_PARAM, None)
        inputs = [kwargs.pop(k) for k in list(kwargs) if k.startswith("input")]
        op_name = kwargs.pop("op_name")
        result = call_op(op_name, inputs, *kwargs.values())
        if result is not None:
            return _show_result(
                result,
                viewer,
                name=f"Result of {op_name}",
                layer_type=category.output,
                op_id=id(gui_function),
            )
        return None

    gui_function.__name__ = f'do_{category.name.lower().replace(" ", "_")}'
    gui_function.__signature__ = Signature(params)

    widget = magicgui(gui_function, auto_call=True)
    op_name_widget = getattr(widget, OP_NAME_PARAM)

    @op_name_widget.changed.connect
    def update_positional_labels(*_):
        new_sig = signature(cle.operation(op_name_widget.value))
        # get the names of positional parameters in the new operation
        param_names = [
            name
            for name, param in new_sig.parameters.items()
            if param.annotation in {int, str, float, bool}
        ]

        # update the labels of each positional-arg subwidget
        # or, if there are too many, hide them
        n_params = len(param_names)
        for n, arg in enumerate(category.args):
            wdg = getattr(widget, arg[0])
            if n < n_params:
                wdg.label = param_names[n]
                wdg.text = param_names[n]
                wdg.show()
            else:
                wdg.hide()

    # run it once to update the labels
    update_positional_labels()

    return widget
