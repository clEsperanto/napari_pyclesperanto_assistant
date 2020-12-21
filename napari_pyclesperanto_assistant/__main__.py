# pyclesperanto assistant standalone
#
# The assistant allows to call operations from the graphical user interface and implement an
# image-data-flow-graph. When parameters of operations high in the hierarchy are updated, downstream
# operations are updated. This facilitates finding a good parameter setting for complex workflows.
#
# -----------------------------------------------------------------------------
from pathlib import Path


def main():
    import napari
    from skimage.io import imread
    import pyclesperanto_prototype as cle
    from napari_pyclesperanto_assistant._gui._AssistantGui import AssistantGUI

    import sys

    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
        image = imread(filename)
    else:
        # make some artificial cell image
        filename = "undefined.tif"
        labels = cle.artificial_tissue_2d(width=512, height=512, delta_x=48, delta_y=32, random_sigma_x=6, random_sigma_y=6)
        membranes = cle.detect_label_edges(labels)
        eroded = cle.maximum_sphere(membranes, radius_x=3, radius_y=3)
        blurred = cle.gaussian_blur(eroded, sigma_x=3, sigma_y=3)
        image = cle.pull_zyx(blurred)

    #image = imread('https://samples.fiji.sc/blobs.png')
    #image = imread('C:/structure/data/lund_000500_resampled.tif')
    #filename = 'data/Lund_000500_resampled-cropped.tif'
    #filename = str(Path(__file__).parent) + '/data/CalibZAPWfixed_000154_max-16.tif'

    print(cle.available_device_names())
    cle.select_device("p520")
    print(cle.get_device())

    with napari.gui_qt():
        # create a viewer and add some image
        viewer = napari.Viewer()
        layer = viewer.add_image(image)
        layer.filename = filename

        from napari_pyclesperanto_assistant import napari_plugin
        napari_plugin(viewer)


if __name__ == '__main__':
      # execute only if run as a script
      main()
