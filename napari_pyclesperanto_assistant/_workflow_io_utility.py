from inspect import Signature, signature
from functools import partial
from magicgui import magicgui
from functools import wraps
from napari.utils._magicgui import _make_choice_data_setter
from napari.types import ImageData, LabelsData

def initialise_root_functions(workflow, viewer):
    """
    Makes widgets for all functions which have a root image as input. The widgets are 
    added to the viewer and correct input images must be chosen to complete the loading
    of the workflow

    Parameters
    ----------
    workflow:
        napari-workflow object
    viewer:
        napari.Viewer instance
    """
    # find all workflow steps with functions which have root images as an input
    root_functions = wf_steps_with_root_as_input(workflow)

    # iterate over root function workflow steps
    for wf_step_name in root_functions:
        # get the fuction from the workflow step and change its signature to
        # the values specified by the workflow
        func = workflow._tasks[wf_step_name][0]
        signat = signature_w_kwargs_from_function(workflow=workflow,
                                                  wf_step_name=wf_step_name)
        func.__signature__ = signat

        # create the widget based on the adjusted function
        widget = make_flexible_gui(func, 
                                   viewer, 
                                   wf_step_name= wf_step_name)

        # make a tooltip which tells the user to select the input image
        # specified by the workflow
        key_source_list = get_source_keywords_and_sources(workflow,
                                                          wf_step_name)
        for key, source in key_source_list:
            widget[key].tooltip = f'Select {source} or equivalent'

        # add the final widget to the napari viewer
        viewer.window.add_dock_widget(widget, name = wf_step_name[10:] + '<b> - SELECT INPUT</b>')

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
    """
    # find all workflow steps with functions which have root images as an input
    root_functions = wf_steps_with_root_as_input(workflow)
    # get the layer object from the napari viewer
    layers = viewer.layers

    # start the iteration with the followers of the root functions
    followers = []
    for root in root_functions:
        followers += workflow.followers_of(root)

    # iteration over followers: the list of followers gets bigger the more functions 
    # have been added with followers of their own
    for i,follower in enumerate(followers):
        # get current layer names
        layer_names = [str(lay) for lay in layers]
        # find all sources of the current function being added
        sources = workflow.sources_of(follower)

        # checking if we have all input images to the function in the napari layers
        sources_present = True
        for source in sources:
            if source not in layer_names:
                sources_present = False

        # if some input images are missing we will move to other functions first
        if not sources_present:
            if follower not in followers[i+1:]:
                followers.append(follower)

        # if all input images are there we can continue
        else:
            # get the fuction from the workflow step and change its signature to
            # the values specified by the workflow
            func = workflow._tasks[follower][0]
            signat = signature_w_kwargs_from_function(workflow=workflow,
                                                        wf_step_name=follower)
            func.__signature__ = signat

            # if more than one source is needed autocall needs to be set to false
            # in order to avoid crashing
            if len(sources) > 1:
                widget = make_flexible_gui(func, 
                                            viewer, 
                                            follower,
                                            autocall= False)
            else:
                widget = make_flexible_gui(func, 
                                            viewer, 
                                            follower)

            # add the final widget to the napari viewer and set the input images in
            # the dropdown to the specified input images
            viewer.window.add_dock_widget(widget, name= follower[10:])
            set_choices(workflow= workflow,
                        wf_step_name= follower,
                        viewer= viewer,
                        widget= widget)

            # calling the widget with the correct input images
            widget()

            # finding new followers of the current workflow step
            new_followers = workflow.followers_of(follower)

            # checking if the new followers are already in the que of workflow steps
            # to be added
            for new_follower in new_followers:
                if new_follower not in followers[i+1:]:
                    followers.append(new_follower)

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
    sig = signature(func)

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
    with the arguments specified in the workflow. Input images are not not specified 
    in the signature as this can only be done with set_choices

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
            kw_dict.pop(name)

    return signature(partial(func, **kw_dict))

def set_choices(workflow, wf_step_name: str, viewer, widget):
    """
    Sets the choices for image drop down menu to the images specified by the workflow

    Parameters
    ----------
    workflow:
        napari-workflow object
    wf_step_name: str
        the string of the workflow step for which the choices in the widget will
        be modified
    viewer:
        napari.Viewer instance
    widget:
        the magicgui FunctionGui object for which the input choices should be changed
    """
    func = workflow._tasks[wf_step_name][0]
    args = workflow._tasks[wf_step_name][1:]
    sources = workflow.sources_of(wf_step_name)

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
    viewer:
        napari.Viewer instance
    gui:
        magicgui Combobox instance for which the choices should
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

def get_source_keywords_and_sources(workflow, wf_step_name):
    """
    Returns a list of tuples containing (function_keyword, image_name) for all 
    sources of a workflow step with name: wf_step_name

    Parameters
    ----------
    workflow: 
        napari_workflows Workflow class
    wf_step_name: str
        name of the workflow step for which function keywords and image names
        should be returned
    """
    func = workflow._tasks[wf_step_name][0]
    args = workflow._tasks[wf_step_name][1:]
    
    sources = workflow.sources_of(wf_step_name)
    keyword_list = list(signature(func).parameters.keys())
    image_keywords = [(key,value) for key, value in zip(keyword_list,args) if value in sources]
    
    return image_keywords