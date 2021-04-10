
# add your tests here...
import warnings


def test_whatever():
    pass

from pathlib import Path
import napari_pyclesperanto_assistant
from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, \
    label_processing, map, mesh, measure, label_measurements, transform, projection

# workaround for leaking Widgets
def _init_test():
    from qtpy.QtWidgets import QApplication
    return set(QApplication.topLevelWidgets())

def _finalize_test(initial, viewer):
    from qtpy.QtWidgets import QApplication
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

    assistant_gui._activate(denoise)
    assistant_gui._activate(background_removal)
    assistant_gui._activate(filter)
    assistant_gui._activate(binarize)
    assistant_gui._activate(label)
    assistant_gui._activate(label_processing)
    assistant_gui._activate(map)
    assistant_gui._activate(combine)

    #assistant_gui._activate(label)
    #assistant_gui._activate(mesh)
    #assistant_gui._activate(measure)
    #assistant_gui._activate(label_measurements)
    #assistant_gui._activate(transform)
    #assistant_gui._activate(projection)

    assistant_gui._export_jython_code_to_clipboard()
    assistant_gui._export_notebook(filename="test.ipynb")

    _finalize_test(initial, viewer)


#def test_whatever3(make_napari_viewer):
#
#    viewer = make_napari_viewer()
#
#    import napari_pyclesperanto_assistant
#    #assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
#    pass


#def test_complex_workflow(make_napari_viewer):
    #import napari_pyclesperanto_assistant
    #from pathlib import Path

    #root = Path(napari_pyclesperanto_assistant.__file__).parent

    #filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')

    # start napari
    #viewer = make_napari_viewer()

    #layer = viewer.open(filename)
    #layer[0].metadata['filename'] = filename

    # attach the assistant
    #assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    #from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, \
    #    label_processing, map, mesh, measure, label_measurements, transform, projection
    #assistant_gui._activate(denoise)
    #assistant_gui._activate(background_removal)
    #assistant_gui._activate(filter)
    #assistant_gui._activate(binarize)
