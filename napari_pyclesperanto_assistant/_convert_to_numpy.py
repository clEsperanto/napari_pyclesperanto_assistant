import numpy as np
from magicgui import magicgui
from napari.types import ImageData, LabelsData, LayerDataTuple
from typing_extensions import Annotated
from napari.layers import Image, Labels, Layer
LayerInput = Annotated[Layer, {"label": "Image"}]

def convert_to_numpy(layer : LayerInput) -> ImageData:
    return np.asarray(layer.data)
