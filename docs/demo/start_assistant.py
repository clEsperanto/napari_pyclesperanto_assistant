import napari
import napari_pyclesperanto_assistant
from pathlib import Path

root = Path(napari_pyclesperanto_assistant.__file__).parent

filename = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
# filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    layer = viewer.open(filename)
    layer[0].metadata['filename'] = filename

    # attach the assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
