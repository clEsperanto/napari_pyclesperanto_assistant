import napari
import napari_pyclesperanto_assistant
from pathlib import Path

<<<<<<< HEAD

root = Path(napari_pyclesperanto_assistant.__file__).parent
img_path = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
=======
root = Path(napari_pyclesperanto_assistant.__file__).parent

filename = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
# filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')
>>>>>>> 1b6b7d026ee5cd1714ce3e62d8722aff7bff89ba

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

<<<<<<< HEAD
    viewer.open(img_path)
=======
    layer = viewer.open(filename)
    layer[0].metadata['filename'] = filename
>>>>>>> 1b6b7d026ee5cd1714ce3e62d8722aff7bff89ba

    # attach the assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
