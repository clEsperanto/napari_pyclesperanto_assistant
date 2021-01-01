import napari

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    viewer.open('../../napari_pyclesperanto_assistant/data/Lund_000500_resampled-cropped.tif')

    # attach the assistant
    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

