import napari

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    import pyclesperanto_prototype as cle
    from numpy.random import random
    import numpy as np

    # Generate artificial cells as test data
    tissue = cle.artificial_tissue_2d()
    viewer.add_labels(tissue)

    # fill it with random measurements
    values = random([int(cle.maximum_of_all_pixels(tissue))])
    for i, y in enumerate(values):
        if (i != 95):
            values[i] = values[i] * 10 + 45
        else:
            values[i] = values[i] * 10 + 90

    measurements = cle.push(np.asarray([values]))

    # visualize measurments in space
    example_image = cle.replace_intensities(tissue, measurements)
    viewer.add_image(cle.pull(example_image), colormap='turbo')

    # attach the assistant
    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

