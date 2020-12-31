import napari

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    viewer.open('../../napari_pyclesperanto_assistant/data/CalibZAPWfixed_000154_max-16.tif')

    # attach the assistant
    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    # define a custom extension for the assistant
    from magicgui import magicgui
    from napari.layers import Image
    @magicgui(
        #auto_call=True,
        call_button='Run',
        layout='vertical',
    )
    def skimage_watershed(image : Image = None, labeled_spots : Image = None, binary_mask: Image = None):

        if image is not None and labeled_spots is not None and binary_mask is not None:
            from skimage.segmentation import watershed
            output = watershed(image.data, labeled_spots.data, mask=binary_mask.data)

            # show result in napari
            if (skimage_watershed.initial_call):
                skimage_watershed.self.viewer.add_labels(output)
                skimage_watershed.initial_call = False
            else:
                skimage_watershed.self.layer.data = output
                skimage_watershed.self.layer.name = "Result of watershed"

    # add my custom button
    assistant_gui.add_button("Scikit-image watershed", skimage_watershed)





