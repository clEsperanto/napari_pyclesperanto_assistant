from magicgui import magicgui
import pyclesperanto_prototype as cle

@magicgui(Select_GPU={
        "choices": cle.available_device_names(),
    },)
def gpu_selector(Select_GPU : str):
    print("Selected device:", cle.select_device(Select_GPU))
    gpu_selector.hide()

def select_gpu():
    if select_gpu.device != None:
        print("Changing the GPU device is currently not supported.\n"
              "See also https://github.com/clEsperanto/pyclesperanto_prototype/issues/110")
        return

    print("selecting gpu")

    print(cle.available_device_names())
    gpu_selector.show()


select_gpu.device = None