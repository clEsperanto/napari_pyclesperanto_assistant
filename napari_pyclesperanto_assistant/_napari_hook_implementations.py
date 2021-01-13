# Implementation of naparis hook specification according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec

from napari_plugin_engine import napari_hook_implementation

from napari_pyclesperanto_assistant import AssistantGUI

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    print("hello world")
    #return AssistantGUI(None)
