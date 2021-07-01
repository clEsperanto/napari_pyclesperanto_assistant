import numpy as np
from magicgui import magicgui
from napari.types import ImageData, LabelsData, LayerDataTuple
from typing_extensions import Annotated
from napari.layers import Image, Labels, Layer
LayerInput = Annotated[Layer, {"label": "Image"}]

def convert_to_numpy(layer : LayerInput) -> Layer:
    if isinstance(layer, Labels):
        return Labels(np.asarray(layer.data))
    else:
        return Image(np.asarray(layer.data))