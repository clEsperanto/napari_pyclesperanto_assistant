# pyclesperanto-assistant
pyclesperanto-assistant is a yet experimental napari plugin for building GPU-accelerated image processing workflows. 
It is part of the [clEsperanto](http://clesperanto.net) project.

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot.png)

## Installation

Download and install `napari-pyclesperanto-assitant` uing `pip`. Windows user should follow the instructions in the section below in case of trouble.

```
pip install napari-pyclesperanto-assistant
```

Afterwards, you can start the assistant using the following command. Replace the url with an image file of your choice:
```
python -m napari_pyclesperanto_assistant https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/napari_pyclesperanto_assistant/data/CalibZAPWfixed_000154_max-16.tif
```

### Installation on windows
On windows some additional steps are necessary. Download a pre-compiled wheel of [pyopencl](https://documen.tician.de/pyopencl/) e.g. from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl). 
It is recommended to install `pyopencl-...+cl21-cp38-cp38-win_amd64` - the `cl12` and `cp38` are important when choosing the right download. They stand for OpenCL 1.2 and Python 3.8.

Enter your username and the correct `pyopencl-...` filename in the following line and execute it from the command line:
```
C:\Users\<username>\AppData\Local\Programs\napari\python\python.exe -m pip install pyopencl-2020.2.2+cl12-cp38-cp38-win_amd64.whl
```

In case napari doesn't start up  ([see also](https://github.com/napari/napari/issues/2022)), enter your username in the following line and execute it from the command line:
```
C:\Users\<username>\AppData\Local\Programs\napari\python\python.exe -m pip install numpy==1.19.3
```

## For developers

Getting the recent code from github and locally installing it
```
git clone https://github.com/haesleinhuepf/pyclesperanto_assistant.git

pip install -e ./pyclesperanto_assistant
```

Optional: Also install pyclesperantos recent source code from github:
```
git clone https://github.com/clEsperanto/pyclesperanto_prototype.git

pip install -e ./pyclesperanto_prototype
```

Starting up napari with the pyclesperanto assistant installed:
```
ipython --gui=qt pyclesperanto_assistant\pyclesperanto_assistant
```

## Feedback welcome!
clEsperanto is developed in the open because we believe in the [open source community](https://clij.github.io/clij2-docs/community_guidelines). Feel free to drop feedback as [github issue](https://github.com/clEsperanto/pyclesperanto_prototype/issues) or via [image.sc](https://image.sc)
