import napari
import numpy as np
import pyclesperanto_prototype as cle
from numpy.random import random

# start napari
viewer = napari.Viewer()

# Generate artificial cells as test data
tissue = cle.artificial_tissue_2d()
viewer.add_labels(tissue.astype("int32"))

# fill it with random measurements
values = random([int(cle.maximum_of_all_pixels(tissue))])
for i, y in enumerate(values):
    values[i] = values[i] * 10 + 45 if (i != 95) else values[i] * 10 + 90
measurements = cle.push(np.asarray([values]))

# visualize measurments in space
example_image = cle.replace_intensities(tissue, measurements)
viewer.add_image(cle.pull(example_image), colormap="turbo")
# attach the assistant
viewer.window.add_plugin_dock_widget("clEsperanto")

napari.run()
