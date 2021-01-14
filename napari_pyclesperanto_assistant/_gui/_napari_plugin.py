from ._Assistant import Assistant

def napari_plugin(viewer) -> Assistant:

    # add the _gui to the viewer as a dock widget
    gui = Assistant(viewer)
    viewer.window.add_dock_widget(gui, name='Add layer', area='right')
    return gui
