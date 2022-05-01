from magicgui import magicgui
import pyclesperanto_prototype as cle
from napari_tools_menu import register_action



@magicgui(Select_GPU={
        "choices": cle.available_device_names(),
    },
    Note={"widget_type":"Label"},
    call_button='Select')
def gpu_selector(Select_GPU : str, Note:str = "Hint: Do not change the GPU while images are open."):
    print("Selected device:", cle.select_device(Select_GPU))
    gpu_selector.hide()

@register_action(menu="Utilities > Select GPU (clesperanto)")
def select_gpu(viewer):
    if select_gpu.device != None:
        print("Changing the GPU device is currently not supported.\n"
              "See also https://github.com/clEsperanto/pyclesperanto_prototype/issues/110")
        return

    if len(cle.available_device_names()) > 1:
        gpu_selector.show()

select_gpu.device = None
