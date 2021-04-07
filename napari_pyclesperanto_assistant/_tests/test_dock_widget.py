# from napari_pyclesperanto_assistant import napari_experimental_provide_dock_widget

import napari

# add your tests here...
def test_whatever():
    pass


def test_whatever2(make_napari_viewer):

    viewer = make_napari_viewer()
    pass

def test_whatever3(make_napari_viewer):

    viewer = make_napari_viewer()

    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)
    pass


def test_complex_workflow(make_napari_viewer):
    print("x")

    import napari_pyclesperanto_assistant
    from pathlib import Path
    print("7")

    root = Path(napari_pyclesperanto_assistant.__file__).parent

    filename = str(root / 'data' / 'Lund_000500_resampled-cropped.tif')
    # filename = str(root / 'data' / 'CalibZAPWfixed_000154_max-16.tif')

    # start napari
    print("b")
    viewer = make_napari_viewer()

    print("c")
    layer = viewer.open(filename)
    layer[0].metadata['filename'] = filename

    # attach the assistant
    print("d")
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    print("e")
    from .._operations._operations import denoise, background_removal, filter, binarize, combine, label, \
        label_processing, map, mesh, measure, label_measurements, transform, projection
    assistant_gui._activate(denoise)
    print("f")
    assistant_gui._activate(background_removal)
    assistant_gui._activate(filter)
    assistant_gui._activate(binarize)
