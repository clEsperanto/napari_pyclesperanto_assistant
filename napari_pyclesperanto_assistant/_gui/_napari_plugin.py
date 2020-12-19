from ._AssistantGui import AssistantGUI

def napari_plugin(viewer):

    # add the _gui to the viewer as a dock widget
    viewer.window.add_dock_widget(AssistantGUI(viewer), area='right')