# Implementation of naparis hook specification according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec
from typing import Union, Tuple, Any, Dict, List, Callable, Optional
from napari_plugin_engine import napari_hook_implementation, napari_hook_specification

LayerData = Union[Tuple[Any], Tuple[Any, Dict], Tuple[Any, Dict, str]]
ReaderFunction = Callable[[str], List[LayerData]]

@napari_hook_implementation
def napari_get_reader(
    path: Union[str, List[str]]
) -> Optional[ReaderFunction]:
    print("I'm asked: ", path)
    if isinstance(path, str) and path.endswith(".idfg.py"):
        print("Yes!")
        return reader_function
    return None

def reader_function(path):
    print("IDFG read", path)
    import napari
    #with napari.gui_qt():
    # create a viewer and add some image
    viewer = napari.Viewer()
    #layer = viewer.open(path)
    #layer.filename = path

    from napari_pyclesperanto_assistant import napari_plugin
    napari_plugin(viewer)

    import numpy as np
    return None