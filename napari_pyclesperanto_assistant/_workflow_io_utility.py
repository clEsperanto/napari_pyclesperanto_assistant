from inspect import Signature, signature
from functools import partial
from re import L
from tkinter import N
from unicodedata import name
from napari_workflows import Workflow
from magicgui import magicgui
from functools import wraps
from napari.utils._magicgui import _make_choice_data_setter
from pytools import word_wrap

def initialise_root_functions(workflow, viewer):
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

        signat = signature_w_kwargs_from_function(workflow=workflow,
                                                  wf_step_name=wf_step_name)
        func.__signature__ = signat

        widget = make_flexible_gui(func, 
                                   viewer, 
                                   wf_step_name= wf_step_name)
        viewer.window.add_dock_widget(widget, name = wf_step_name[10:])

def load_remaining_workflow(workflow, viewer):
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
    
    followers = []
    for root in root_functions:
        followers += workflow.followers_of(root)

    reviseted_followers = []
    for follower in followers:
        print('is anybody there?')
        layer_names = [str(lay) for lay in layers]
        sources = workflow.sources_of(follower)

        # checking if we have all input images to the function in the napari layers
        sources_present = True
        for source in sources:
            if source not in layer_names:
                sources_present = False

        # if some input images are missing we will process other images first
        if not sources_present:
            print(f'we are here because of {follower} and the sources {sources}')
            if follower not in reviseted_followers:
                followers.append(follower)
                print(f'appended {follower} because {sources} includes non existing layer')
        # if all input images are there we can continue
        else:
            func = workflow._tasks[follower][0]
            signat = signature_w_kwargs_from_function(workflow=workflow,
                                                      wf_step_name=follower)
            func.__signature__ = signat

            if len(sources) > 1:
                widget = make_flexible_gui(func, 
                                           viewer, 
                                           follower,
                                           autocall= False)
            else:
                widget = make_flexible_gui(func, 
                                           viewer, 
                                           follower)

            viewer.window.add_dock_widget(widget, name= follower[10:])
            set_choices(workflow= workflow,
                        wf_step= follower,
                        viewer= viewer,
                        widget= widget)
            widget()

            new_follower = workflow.followers_of(follower)
            followers += new_follower
            if follower in reviseted_followers:
                reviseted_followers.remove(follower)

def make_flexible_gui(func, viewer, wf_step_name, autocall = True):
    """
    Function returns a widget with a GUI for the function provided in the parameters,
    that can be added to the napari viewer. Largely copied from @haesleinhuepf (I can't remember where though)
    

    Parameters
    ----------
    func: 
        input function to generate the gui for
    viewer:
        napari.Viewer instance to which the widget is added
    wf_step_name: str
        name of the workflow step matching the function
    autocall: Boolean
        sets the auto_call behaviour of the magicgui.magicgui function
    """
    gui = None
    name = wf_step_name[10:]
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
            op_name = name
            new_name = f"Result of {op_name}"

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

    gui = magicgui(worker_func, auto_call= autocall)
    return gui

def signature_w_kwargs_from_function(workflow, wf_step_name) -> Signature:
    """
    Returns a new signature for a function in which the default values are replaced
    with the arguments given in arg_vals

    Parameters
    ----------
    workflow: 
        napari-workflows object containing the function

    wf_step_name: str
        key of the workflow step for which the signature should be generated
    """
    func     = workflow._tasks[wf_step_name][0]
    arg_vals = workflow._tasks[wf_step_name][1:] 
    # getting the keywords corresponding to the values
    keyword_list = list(signature(func).parameters.keys())

    # creating the kwargs dict
    kw_dict = {}
    for kw, val in zip(keyword_list, arg_vals):
        kw_dict[kw] = val

    dict_keys = list(kw_dict.keys())    
    input_image_names = workflow.sources_of(wf_step_name)
    for name in dict_keys:
        if ((kw_dict[name] in input_image_names) and (name != 'viewer')):
            kw_dict.pop(name) # we are making an assumption that the input will aways be this

    return signature(partial(func, **kw_dict))

def set_choices(workflow, wf_step: str, viewer, widget):
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
    sources = workflow.sources_of(wf_step)

    keyword_list = list(signature(func).parameters.keys())
    image_keywords = [(key,value) for key, value in zip(keyword_list,args) if value in sources]
    
    for key, name in image_keywords:
        widget[key].choices = get_layers_data_of_name(name, viewer, widget[key])

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