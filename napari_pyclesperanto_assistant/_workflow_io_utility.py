from inspect import Signature, signature
from functools import partial
from tkinter import N
from unicodedata import name
from napari_workflows import Workflow
from magicgui.widgets import FunctionGui
from functools import wraps
from napari.utils._magicgui import _make_choice_data_setter

def initialise_root_functions(workflow, viewer, func_name_mapping):
    """
    Makes widgets based on a list of functions, which should be the functions processing
    root images. The widgets are added to the viewer and correct input images must be
    chosen before loading the remaining workflow

    Parameters
    ----------
    workflow:
        napari-workflow object
    viewer:
        napari.Viewer instance
    root_functions: list
        list of workflow step names corresponding to functions with root images as input
    """
    root_functions = wf_steps_with_root_as_input(workflow)

    for wf_step_name in root_functions:
        func = workflow._tasks[wf_step_name][0]
        args = workflow._tasks[wf_step_name][1:] 

        signat = signature_w_kwargs_from_function(func, args)
        func.__signature__ = signat

        widget = make_flexible_gui(func, 
                                   viewer, 
                                   func_name_mapping[wf_step_name],
                                   autocall = True)
        viewer.window.add_dock_widget(widget, name = func_name_mapping[wf_step_name])

def load_remaining_workflow(workflow, viewer, name_mapping, func_name_mapping):
    """
    Loads the remaining workflow once initialise_root_functions has been called with
    the same workflow and the same napari viewer

    Parameters
    ----------
    workflow:
        napari-workflow object
    viewer:
        napari.Viewer instance
    name_mapping:
        a dictionary which maps the workflow image names to the respective layer names
        in the napari.Viewer instance
    """
    root_functions = wf_steps_with_root_as_input(workflow)
    layers = viewer.layers
    
    for root in root_functions:
        followers = workflow.followers_of(root)

        for follower in followers:
            layer_names = [str(lay) for lay in layers]
            sources = workflow.sources_of(follower)
            for source in sources:
                if name_mapping[source] not in layer_names:
                    root_functions.append(root)
                    break
                else:
                    func = workflow._tasks[follower][0]
                    args = workflow._tasks[follower][1:]

                    signat = signature_w_kwargs_from_function(func, args)
                    func.__signature__ = signat
                    print(f'current follower: {follower}; current function: {func.__name__}')
                    widget = make_flexible_gui(func, 
                                               viewer, 
                                               func_name_mapping[follower],
                                               autocall = True)
                    viewer.window.add_dock_widget(widget, name = func_name_mapping[follower])

                    set_choices(workflow= workflow,
                                wf_step= follower,
                                viewer= viewer,
                                widget= widget,
                                name_mapping= name_mapping)

                    widget(layers[name_mapping[source]].data)

                    new_follower = workflow.followers_of(follower)
                    followers += new_follower

class flexible_gui(FunctionGui):
    def __init__(self,function,name,autocall = True, param_options = {}):
        super().__init__(
          function,
          call_button=True,
          layout='vertical',
          auto_call=autocall,
          param_options=param_options
        )

def make_flexible_gui(func, viewer, name, autocall = True):
    """
    Function returns a widget with a GUI for the function provided in the parameters,
    that can be added to the napari viewer. Largely copied from @haesleinhuepf (I can't remember where though)
    

    Parameters
    ----------
    func: 
        input function to generate the gui for
    viewer:
        napari.Viewer instance to which the widget is added
    
    autocall: Boolean
        set wether the function is automatically called when a parameter is changed
    """
    gui = None

    from napari.types import ImageData, LabelsData
    import inspect
    sig = inspect.signature(func)

    @wraps(func)
    def worker_func(*iargs, **ikwargs):
        data = func(*iargs, **ikwargs)
        if data is None:
            return None

        target_layer = None

        if sig.return_annotation in [ImageData, "napari.types.ImageData", LabelsData, "napari.types.LabelsData"]:
            op_name = func.__name__
            new_name = f"{op_name} result"

            # we now search for a layer that has -this- magicgui attached to it
            try:
                # look for an existing layer
                target_layer = next(x for x in viewer.layers if x.source.widget is gui)
                target_layer.data = data
                target_layer.name = new_name
                # layer.translate = translate
            except StopIteration:
                # otherwise create a new one
                from napari.layers._source import layer_source
                with layer_source(widget=gui):
                    if sig.return_annotation in [ImageData, "napari.types.ImageData"]:
                        target_layer = viewer.add_image(data, name=new_name)
                    elif sig.return_annotation in [LabelsData, "napari.types.LabelsData"]:
                        target_layer = viewer.add_labels(data, name=new_name)

        if target_layer is not None:
            # update the workflow manager in case it's installed
            try:
                from napari_workflows import WorkflowManager
                workflow_manager = WorkflowManager.install(viewer)
                workflow_manager.update(target_layer, func, *iargs, **ikwargs)
            except ImportError:
                pass

            return None
        else:
            return data

    gui = flexible_gui(worker_func, name, autocall)
    return gui


def signature_w_kwargs_from_function(function, arg_vals: list) -> Signature:
    """
    Returns a new signature for a function in which the default values are replaced
    with the arguments given in arg_vals

    Parameters
    ----------
    function: 
        input function to generate new signature

    arg_vals: list
        list of arguments to replace defaults in signature
    """

    # getting the keywords corresponding to the values
    keyword_list = list(signature(function).parameters.keys())

    # creating the kwargs dict
    kw_dict = {}
    for kw, val in zip(keyword_list, arg_vals):
        kw_dict[kw] = val
        
    possible_input_image_names = ['image',
                                  'label_image',
                                  'binary_image'
                                 ]
    for name in possible_input_image_names:
        try:
            kw_dict.pop(name) # we are making an assumption that the input will aways be this
        except KeyError:
            pass

    return signature(partial(function, **kw_dict))

def function_name_mapping(workflow):
    func_mapping = {}
    roots = workflow.roots()
    for result, task_tuple in workflow._tasks.items():
        if result not in roots:
            func = task_tuple[0]
            funcname = func.__name__
            if result.endswith(']'):
                new_funcname = funcname + ' ' + result[-3:]
                func_mapping[result] = new_funcname
            else:
                func_mapping[result] = funcname
    return func_mapping 

def old_wf_names_to_new_mapping(workflow):
    """
    Returns a dictionary mapping old workflow step names to new ones

    Parameters
    ----------
    workflow: 
        napari_workflows Workflow class
    """
    mapping = {}
    for old_key, content in workflow._tasks.items():
        func = content[0]
        new_name = func.__name__ + ' result'
        mapping[old_key] = new_name
    
    return mapping

def wf_steps_with_root_as_input(workflow):
    """
    Returns a list of workflow steps that have root images as an input

    Parameters
    ----------
    workflow: 
        napari_workflows Workflow class
    """
    roots = workflow.roots()
    wf_step_with_rootinput = []
    for result, task in workflow._tasks.items():
            for source in task:
                if isinstance(source, str):
                    if source in roots:
                        wf_step_with_rootinput.append(result)
    return wf_step_with_rootinput

def get_layers_data_of_name(layer_name: str, viewer, gui):
    """
    Returns a choices dictionary which can be utilised to set an input image of a 
    widget with the function set_choices. code modified from napari/utils/_magicgui
    get_layers_data function.

    Parameters
    ----------
    layer_name: str
        the layer which should be selected as the only choice in a drop down menu
    """
    choices = []
    for layer in [x for x in viewer.layers if str(x) == layer_name]:
        choice_key = f'{layer.name} (data)'
        choices.append((choice_key, layer.data))
        layer.events.data.connect(_make_choice_data_setter(gui, choice_key))

    return choices

def set_choices(workflow, wf_step: str, viewer, widget, name_mapping = None):
    """
    Sets the choices for image drop downs to the images specified by the workflow

    Parameters
    ----------
    workflow:
        napari-workflow object
    wf_step: str
        the string of the workflow step for which the choices in the widget will
        be modified
    viewer:
        napari.Viewer instance
    widget:
        the magicgui FunctionGui object for which the input choices should be changed
    name_mapping:
        a dictionary which maps the workflow image names to the respective layer names
        in the napari.Viewer instance
    """
    func = workflow._tasks[wf_step][0]
    args = workflow._tasks[wf_step][1:]

    keyword_list = list(signature(func).parameters.keys())
    image_keywords = [(key,value) for key, value in zip(keyword_list,args) if isinstance(value, str)]
    image_names = [key for key, value in zip(keyword_list,args) if isinstance(value, str)]

    if name_mapping is None:
        conversion_dict = {name: name for name in image_names}
    else:
        conversion_dict = name_mapping

    
    for key, name in image_keywords:
        widget[key].choices = get_layers_data_of_name(conversion_dict[name], viewer, widget[key])