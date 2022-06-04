from __future__ import annotations
from ._select_gpu import select_gpu
from napari.viewer import Viewer
import napari_assistant


class Assistant(napari_assistant.Assistant):
    """The main cle Assistant widget.

    The widget holds buttons with icons to create widgets for the various
    cel operation categories.  It tracks which layers are connected to which
    widgets, and can export the state of the task graph to a dask graph
    or to python code.

    Parameters
    ----------
    napari_viewer : Viewer
        This viewer instance will be provided by napari when it gets added
        as a plugin dock widget.
    """

    def __init__(self, napari_viewer: Viewer):
        super().__init__(napari_viewer)

        if not Assistant._gpu_selected:
            select_gpu(napari_viewer)
            Assistant._gpu_selected = True

Assistant._gpu_selected = False
