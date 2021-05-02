import pytest
from napari import Viewer
from napari_pyclesperanto_assistant._categories import CATEGORIES, LabelsInput

@pytest.fixture
def viewer(qtbot):
    viewer = Viewer(show=False)
    yield viewer
    viewer.close()

@pytest.fixture
def assistant(viewer):
    viewer = Viewer(show=False)
    viewer.window.add_plugin_dock_widget("clEsperanto", "Assistant")
    dw = viewer.window._dock_widgets["clEsperanto: Assistant"]
    return dw.widget()


@pytest.mark.parametrize("category", CATEGORIES.values(), ids=lambda c: c.name)
def test_individual_categories(category, assistant):
    assistant.load_sample_data()
    if LabelsInput in category.inputs:
        assistant._activate(CATEGORIES.get("Binarize"))
    assistant._activate(category)
    assistant.to_clipboard()
 
def test_workflow_processing_labels(viewer):
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
