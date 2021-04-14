import pytest
from napari import Viewer

@pytest.fixture
def viewer(qtbot):
    return  Viewer(show=False)

def test_workflow_processing_labels(viewer):
    import napari
    import napari_pyclesperanto_assistant
    from pathlib import Path

    root = Path(napari_pyclesperanto_assistant.__file__).parent
    img_path = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')

    # start napari
    viewer.open(img_path)
    viewer.window.add_plugin_dock_widget("clEsperanto", "Background removal")
    viewer.window.add_plugin_dock_widget("clEsperanto", "Binarize")
    viewer.window.add_plugin_dock_widget("clEsperanto", "Label")
    viewer.window.add_plugin_dock_widget("clEsperanto", "Label measurements")
