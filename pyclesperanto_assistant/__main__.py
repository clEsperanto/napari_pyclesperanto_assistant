# pyclesperanto assistant standalone
#
# The assistant allows to call operations from the graphical user interface and implement an
# image-data-flow-graph. When parameters of operations high in the hierarchy are updated, downstream
# operations are updated. This facilitates finding a good parameter setting for complex workflows.
#
# -----------------------------------------------------------------------------

def main():
    import napari
    from skimage.io import imread
    import pyclesperanto_prototype as cle
    from pyclesperanto_assistant._gui._MainMenu import Gui

    #filename = 'data/Lund_000500_resampled-cropped.tif'
    filename = 'data/CalibZAPWfixed_000154_max-16.tif'
    image = imread(filename)
    #image = imread('https://samples.fiji.sc/blobs.png'')
    #image = imread('C:/structure/data/lund_000500_resampled.tif')

    print(cle.available_device_names())
    cle.select_device("p520")
    print(cle.get_device())

    with napari.gui_qt():
        # create a viewer and add some image
        viewer = napari.Viewer()
        layer = viewer.add_image(image)
        layer.filename = filename

        def _on_removed(event):
            layer = event.value
            try:
                layer.dialog._removed()
            except AttributeError:
                pass
        viewer.layers.events.removed.connect(_on_removed)

        # add the _gui to the viewer as a dock widget
        viewer.window.add_dock_widget(Gui(viewer), area='right')


if __name__ == '__main__':
      # execute only if run as a script
      main()
