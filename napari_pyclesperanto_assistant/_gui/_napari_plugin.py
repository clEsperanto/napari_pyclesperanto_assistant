from ._AssistantGui import AssistantGUI

def napari_plugin(viewer) -> AssistantGUI:

    # add the _gui to the viewer as a dock widget
    gui = AssistantGUI(viewer)
    viewer.window.add_dock_widget(gui, area='right')
    return gui
