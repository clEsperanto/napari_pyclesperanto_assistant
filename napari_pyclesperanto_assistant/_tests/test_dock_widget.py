
# add your tests here...
def test_whatever():
    pass

from pathlib import Path
import napari_pyclesperanto_assistant
from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, \
    label_processing, map, mesh, measure, label_measurements, transform, projection


def test_whatever2(make_napari_viewer):

    viewer = make_napari_viewer()

    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    root = Path(napari_pyclesperanto_assistant.__file__).parent
    filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')
    layer = viewer.open(filename)

    #assistant_gui._activate(denoise)
    #assistant_gui._activate(background_removal)
    #assistant_gui._activate(filter)
    #assistant_gui._activate(binarize)


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
