import napari
import napari_pyclesperanto_assistant
from magicgui import magicgui
from napari.layers import Image

# start napari
viewer = napari.Viewer()

viewer.open('../../napari_pyclesperanto_assistant/data/CalibZAPWfixed_000154_max-16.tif')

# attach the assistant
assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
# define a custom extension for the assistant
@magicgui(
    auto_call=True,
    layout='vertical',
)
def skimage_threshold_yen(input1 : Image = None):

    if input1 is not None:
        from skimage.filters import threshold_yen

        output = input1.data > threshold_yen(input1.data)

        # show result in napari
        if (skimage_threshold_yen.initial_call):
            skimage_threshold_yen.self.viewer.add_labels(output)
            skimage_threshold_yen.initial_call = False
        else:
            skimage_threshold_yen.self.layer.data = output
            skimage_threshold_yen.self.layer.name = "Result of threshold_yen"

# add my custom button
assistant_gui.add_button("Scikit-image threshold_yen", skimage_threshold_yen)

napari.run()



