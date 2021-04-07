# from napari_pyclesperanto_assistant import napari_experimental_provide_dock_widget

# add your tests here...
def test_whatever():
    pass

import pytest

@pytest.fixture
def make_test_viewer(qtbot, request):
    from napari import Viewer
    viewers = []

    def actual_factory(*model_args, viewer_class=Viewer, **model_kwargs):
        model_kwargs.setdefault('show', False)
        viewer = viewer_class(*model_args, **model_kwargs)
        viewers.append(viewer)
        return viewer

    yield actual_factory

    for viewer in viewers:
        viewer.close()

def test_complex_workflow(make_test_viewer):
    import napari
    import napari_pyclesperanto_assistant
    from pathlib import Path

    root = Path(napari_pyclesperanto_assistant.__file__).parent

    #filename = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
    filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')

    # create Qt GUI context
    #napari.gui_qt()

    # start napari
    viewer = make_test_viewer() # napari.Viewer()

    layer = viewer.open(filename)
    layer[0].metadata['filename'] = filename

    # attach the assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, \
        label_processing, map, mesh, measure, label_measurements, transform, projection
    assistant_gui._activate(denoise)

    viewer.close()
