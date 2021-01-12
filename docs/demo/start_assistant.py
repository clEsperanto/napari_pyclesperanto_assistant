import napari
import napari_pyclesperanto_assistant
from pathlib import Path


root = Path(napari_pyclesperanto_assistant.__file__).parent
img_path = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    viewer.open(img_path)

    # attach the assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
