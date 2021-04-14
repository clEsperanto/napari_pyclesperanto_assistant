import pytest
from napari import Viewer
from napari_pyclesperanto_assistant._categories import CATEGORIES, LabelsInput


@pytest.fixture
def assistant(qtbot):
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
