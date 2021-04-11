import warnings

from pathlib import Path
import napari_pyclesperanto_assistant
from .._operations._operations import StatefulFunctionFactory, magic_denoise, magic_background_removal, \
    magic_filter, magic_binarize, magic_combine, magic_label, \
    magic_label_processing, magic_map, magic_mesh, magic_measure, magic_label_measurements, \
    magic_transform, magic_projection

# workaround for leaking Widgets
def _init_test():
    from qtpy.QtWidgets import QApplication
    return set(QApplication.topLevelWidgets())

def _finalize_test(initial, viewer):
    from qtpy.QtWidgets import QApplication

    viewer.close()

    QApplication.processEvents()
    leaks = set(QApplication.topLevelWidgets()).difference(initial)

    debug_output = ''

    for element in leaks:
        if element.parent() is None:
            debug_output = debug_output + '\nLeaking widget:' + str(element)

        # avoid later assert
        element.setParent(viewer.window.qt_viewer)

    if len(debug_output) > 0:
        warnings.warn(debug_output)

def test_complex_workflow(make_napari_viewer):

    viewer = make_napari_viewer()

    initial = _init_test()

    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    root = Path(napari_pyclesperanto_assistant.__file__).parent
    filename = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
    layer = viewer.open(filename)

    assistant_gui._activate(StatefulFunctionFactory(magic_denoise))
    assistant_gui._activate(StatefulFunctionFactory(magic_background_removal))
    assistant_gui._activate(StatefulFunctionFactory(magic_filter))
    assistant_gui._activate(StatefulFunctionFactory(magic_binarize))
    assistant_gui._activate(StatefulFunctionFactory(magic_label))
    assistant_gui._activate(StatefulFunctionFactory(magic_label_processing))
    assistant_gui._activate(StatefulFunctionFactory(magic_map))
    assistant_gui._activate(StatefulFunctionFactory(magic_combine))

    assistant_gui._activate(StatefulFunctionFactory(magic_transform))
    assistant_gui._activate(StatefulFunctionFactory(magic_projection))

    #assistant_gui._export_jython_code_to_clipboard()
    assistant_gui._export_notebook(filename="test.ipynb")

    _finalize_test(initial, viewer)

