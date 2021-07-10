from __future__ import annotations

from inspect import Parameter, Signature, signature
from typing import Optional, TYPE_CHECKING, Sequence

import pyclesperanto_prototype as cle
import toolz
from loguru import logger
from magicgui import magicgui
from typing_extensions import Annotated

from .._categories import Category
from qtpy.QtWidgets import QPushButton

if TYPE_CHECKING:
    from napari.layers import Layer
    from napari import Viewer

VIEWER_PARAM = "viewer"
OP_NAME_PARAM = "op_name"
OP_ID = "op_id"

def num_positional_args(func, types=[cle.Image, int, str, float, bool]) -> int:
    params = signature(func).parameters
    return len([p for p in params.values() if p.annotation in types])


@logger.catch
def call_op(op_name: str, inputs: Sequence[Layer], timepoint : int = None, *args) -> cle.Image:
    """Call cle operation `op_name` with specified inputs and args.

    Takes care of transfering data to GPU and omitting extra positional args

    Parameters
    ----------
    op_name : str
        name of operation to execute.  (must be valid for `cle.operation`)
    inputs : Sequence[Layer]
        The napari layer inputs

    Returns
    -------
    cle.Image
        The result (still on the GPU)
    """

    if not inputs or inputs[0] is None:
        return

    # transfer data to gpu
    if timepoint is None:
        i0 = inputs[0].data
        gpu_ins = [cle.push(i.data if i is not None else i0) for i in inputs]
    else:
        i0 = inputs[0].data[timepoint] if len(inputs[0].data.shape) == 4 else inputs[0].data
        gpu_ins = [cle.push((i.data[timepoint] if len(i.data.shape) == 4 else i.data) if i is not None else i0) for i in inputs]

    # convert 3d-1-slice-data into 2d data
    # to support 2d timelapse data
    gpu_ins = [i if len(i.shape) != 3 or i.shape[0] != 1 else i [0] for i in gpu_ins]

    # todo: we could make this a little faster by getting gpu_out from a central manager
    gpu_out = None

    # call actual cle function ignoring extra positional args
    cle_function = cle.operation(op_name)  # couldn't this just be getattr(cle, ...)?
    nargs = num_positional_args(cle_function)
    logger.info(f"cle.{op_name}(..., {', '.join(map(str, args))})")
    args = ((*gpu_ins, gpu_out) + args)[:nargs]
    gpu_out = cle_function(*args)

    # return output
    return gpu_out


def _show_result(
    gpu_out: cle.Image,
    viewer: Viewer,
    name: str,
    layer_type: str,
    op_id: int,
    translate=None,
    cmap=None,
    blending=None,
    scale=None,
) -> Optional[Layer]:
    """Show `gpu_out` in the napari viewer.

    Parameters
    ----------
    gpu_out : cle.Image
        a cle.Image to show
    viewer : napari.Viewer
        The napari viewer instance
    name : str
        The name of the layer to create or update.
    layer_type : str
        the layer type to create (must be 'labels' or 'image)
    op_id : int
        an ID to associate with the newly created layer (will be added to
        layer.metada['op_id'])
    translate : [type], optional
        translate parameter for layer creation, by default None
    cmap : str, optional
        a colormap to use for images, by default None
    blending : str, optional
        blending mode for visualization, by default None

    Returns
    -------
    layer : Optional[Layer]
        The created/udpated layer, or None if no viewer is present.
    """
    if not viewer:
        logger.warning("no viewer, cannot add image")
        return
    # show result in napari
    clims = [cle.minimum_of_all_pixels(gpu_out), cle.maximum_of_all_pixels(gpu_out)]

    if clims[1] == 0:
        clims[1] = 1

    # conversion will be done inside napari. We can continue working with the OCL-array from here.
    data = gpu_out

    try:
        # look for an existing layer
        layer = next(x for x in viewer.layers if isinstance(x.metadata, dict) and x.metadata.get(OP_ID) == op_id)
        logger.debug(f"updating existing layer: {layer}, with id: {op_id}")
        layer.data = data
        layer.name = name
        # layer.translate = translate
    except StopIteration:
        # otherwise create a new one
        logger.debug(f"creating new layer for id: {op_id}")
        add_layer = getattr(viewer, f"add_{layer_type}")
        kwargs = dict(name=name, metadata={OP_ID: op_id})
        if layer_type == "image":
            kwargs["colormap"] = cmap
            kwargs["blending"] = blending
            kwargs['contrast_limits'] = clims
        layer = add_layer(data, **kwargs)

    if scale is not None:
        if len(layer.data.shape) <= len(scale):
            layer.scale = scale[-len(layer.data.shape):]
    return layer


def _generate_signature_for_category(category: Category) -> Signature:
    """Create an inspect.Signature object representing a cle Category.

    The output of this function can be used to set function.__signature__ so that
    magicgui can convert it into the appropriate widget.
    """
    k = Parameter.KEYWORD_ONLY

    # add inputs (we name them inputN ...)
    params = [
        Parameter(f"input{n}", k, annotation=t) for n, t in enumerate(category.inputs)
    ]
    # Add valid operations choices (will create the combo box)
    choices = list(cle.operations(['in assistant'] + list(category.include), category.exclude))
    # temporary workaround: remove entries that start with "label_", those have been renamed in pyclesperanto
    # and are only there for backwards compatibility
    choices = list([c for c in choices if not c.startswith('label_')])
    op_type = Annotated[str, {"choices": choices, "label": "Operation"}]
    params.append(
        Parameter(OP_NAME_PARAM, k, annotation=op_type, default=category.default_op)
    )
    # add the args that will be passed to the cle operation.
    for name, type_, default in category.args:
        params.append(Parameter(name, k, annotation=type_, default=default))

    # add a viewer.  This allows our widget to know if it's in a viewer
    params.append(
        Parameter(VIEWER_PARAM, k, annotation="napari.viewer.Viewer", default=None)
    )
    return Signature(params)

def make_gui_for_category(category: Category) -> magicgui.widgets.FunctionGui[Layer]:
    """Generate a magicgui widget for a Category object

    Parameters
    ----------
    category : Category
        An instance of a _categories.Category. (holds information about the cle operations,
        input types, and arguments that the widget needs to represent.)

    Returns
    -------
    magicgui.widgets.FunctionGui
        A magicgui widget instance
    """
    widget = None
    def gui_function(**kwargs) -> Optional[Layer]:
        """A function that calls a cle operation `call_op` and shows the result.

        This is the function that will be called by our magicgui widget.
        We modify it's __signature__ below.
        """
        viewer = kwargs.pop(VIEWER_PARAM, None)
        inputs = [kwargs.pop(k) for k in list(kwargs) if k.startswith("input")]
        t_position = None
        if viewer is not None and len(viewer.dims.current_step) == 4:
            # in case we process a 4D-data set, we need read out the current timepoint
            # and consider it further down in call_op
            t_position = viewer.dims.current_step[0]

            currstep_event = viewer.dims.events.current_step

            def update(event):
                currstep_event.disconnect(update)
                widget()

            if hasattr(widget, 'updater'):
                currstep_event.disconnect(widget.updater)

            widget.updater = update

            currstep_event.connect(update)

        # todo: deal with 5D and nD data

        op_name = kwargs.pop("op_name")
        result = call_op(op_name, inputs, t_position, *kwargs.values())

        # add a help-button
        description = cle.operation(op_name).__doc__.replace("\n    ", "\n")
        temp = description.split('https:')
        link = "https://napari-hub.org/plugins/napari-pyclesperanto-assistant"
        print(temp)
        if len(temp) > 1:
            link = "https:" + temp[1].split("\n")[0]
        def call_link():
            import webbrowser
            webbrowser.open(link)
        if hasattr(widget, 'help'):
            widget.native.layout().removeWidget(widget.help)
        widget.help = QPushButton("Help")
        widget.help.setToolTip(description)
        widget.help.clicked.connect(call_link)
        widget.native.layout().addWidget(widget.help)

        if result is not None:
            return _show_result(
                result,
                viewer,
                name=f"Result of {op_name}",
                layer_type=category.output,
                op_id=id(gui_function),
                cmap=category.color_map,
                blending=category.blending,
                scale=inputs[0].scale,
            )
        return None

    gui_function.__name__ = f'do_{category.name.lower().replace(" ", "_")}'
    gui_function.__signature__ = _generate_signature_for_category(category)

    # create the widget
    widget = magicgui(gui_function, auto_call=True)

    # when the operation name changes, we want to update the argument labels
    # to be appropriate for the corresponding cle operation.
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
