from napari import Viewer
from napari_pyclesperanto_assistant._gui import Assistant


def test_complex_workflow(qtbot, tmp_path):

    viewer = Viewer(show=False)
    viewer.window.add_plugin_dock_widget("clEsperanto")
    dw = viewer.window._dock_widgets["clEsperanto: Assistant"]
    assistant_gui: Assistant = dw.widget()
    assistant_gui.load_sample_data()

    assistant_gui._activate("denoise")
    assistant_gui._activate("background_removal")
    assistant_gui._activate("filter")
    assistant_gui._activate("binarize")
    assistant_gui._activate("label")
    assistant_gui._activate("label_processing")
    assistant_gui._activate("map")
    assistant_gui._activate("combine")

    # assistant_gui._activate('label')
    # assistant_gui._activate('mesh')
    # assistant_gui._activate('measure')
    # assistant_gui._activate('label_measurements')

    assistant_gui._activate("transform")
    assistant_gui._activate("projection")

    assistant_gui._export_jython_code_to_clipboard()
    # assistant_gui._export_notebook(filename='test.ipynb')
