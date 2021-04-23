import napari
import napari_pyclesperanto_assistant
from pathlib import Path


root = Path(napari_pyclesperanto_assistant.__file__).parent
img_path = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')

# start napari
viewer = napari.Viewer()
viewer.open(img_path)
viewer.window.add_plugin_dock_widget("clEsperanto")

napari.run()