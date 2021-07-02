# napari-pyclesperanto-assistant
[![Image.sc forum](https://img.shields.io/badge/dynamic/json.svg?label=forum&url=https%3A%2F%2Fforum.image.sc%2Ftag%2Fclesperanto.json&query=%24.topic_list.tags.0.topic_count&colorB=brightgreen&suffix=%20topics&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAABPklEQVR42m3SyyqFURTA8Y2BER0TDyExZ+aSPIKUlPIITFzKeQWXwhBlQrmFgUzMMFLKZeguBu5y+//17dP3nc5vuPdee6299gohUYYaDGOyyACq4JmQVoFujOMR77hNfOAGM+hBOQqB9TjHD36xhAa04RCuuXeKOvwHVWIKL9jCK2bRiV284QgL8MwEjAneeo9VNOEaBhzALGtoRy02cIcWhE34jj5YxgW+E5Z4iTPkMYpPLCNY3hdOYEfNbKYdmNngZ1jyEzw7h7AIb3fRTQ95OAZ6yQpGYHMMtOTgouktYwxuXsHgWLLl+4x++Kx1FJrjLTagA77bTPvYgw1rRqY56e+w7GNYsqX6JfPwi7aR+Y5SA+BXtKIRfkfJAYgj14tpOF6+I46c4/cAM3UhM3JxyKsxiOIhH0IO6SH/A1Kb1WBeUjbkAAAAAElFTkSuQmCC)](https://forum.image.sc/tag/clesperanto)
[![website](https://img.shields.io/website?url=http%3A%2F%2Fclesperanto.net)](http://clesperanto.net)
[![License](https://img.shields.io/pypi/l/napari-pyclesperanto-assistant.svg?color=green)](https://github.com/haesleinhuepf/napari-pyclesperanto-assistant/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-pyclesperanto-assistant.svg?color=green)](https://pypi.org/project/napari-pyclesperanto-assistant)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-pyclesperanto-assistant.svg?color=green)](https://python.org)
[![tests](https://github.com/clesperanto/napari_pyclesperanto_assistant/workflows/tests/badge.svg)](https://github.com/clesperanto/napari_pyclesperanto_assistant/actions)
[![codecov](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant)

The py-clEsperanto-assistant is a yet experimental [napari](https://github.com/napari/napari) plugin for building GPU-accelerated image processing workflows. 
It is part of the [clEsperanto](http://clesperanto.net) project.
It uses [pyclesperanto](https://github.com/clEsperanto/pyclesperanto_prototype) and with that [pyopencl](https://documen.tician.de/pyopencl/) as backend for processing images.
This plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) using with napari's [cookiecutter-napari-plugin](https://github.com/napari/cookiecutter-napari-plugin) template.

## Installation

It is recommended to install the plugin via conda:
```shell
conda create --name bio11 python==3.8.5 
conda activate bio11 
conda install -c conda-forge pyopencl==2021.2.1
pip install napari-pyclesperanto-assistant
pip install napari[all]
```

You can then start napari and find the assistant in the `Plugins` menu.
```shell
napari
```

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot.png)

## Features
[pyclesperanto](https://github.com/clEsperanto/pyclesperanto_prototype) offers various possibilities for processing images. It comes from developers who work in life sciences and thus, it may be focused towards processing two- and three-dimensional microscopy image data showing cells and tissues. A selection of pyclesperanto's functionality is available via the assistant user interface. Typical workflows which can be built with this assistant include
* image filtering
  * denoising / noise reduction
  * background subtraction
  * grey value morphology 
* combining images
  * masking
  * image math (adding, subtracting, multiplying, dividing images) 
* image transformations
  * translation
  * rotation
  * sub-stacks
* image projections
  * minimum / mean / maximum / sum / standard deviation projections
* image segmentation
  * binarization 
  * thresholding
  * labeling
  * regionalization
  * instance segmentation
  * semantic segmentation
  * detect label edges
  * label spots
  * connected component labeling
  * Voronoi-Otsu-labeling
* post-processing of binary images
  * dilation
  * erosion
  * binary opening
  * binary closing 
  * binary and / or / xor
* post-processing of label images
  * dilation (expansion) of labels
  * erosion (shrinking) of labels 
  * extend labels via Voronoi
  * exclude labels on edges
  * exclude labels within / out of size / value range
* parametric maps
  * proximal / touching neighbor count
  * distance measurements to touching / proximal / n-nearest neighbors
  * pixel count map
  * mean / maximum / extension ratio map
* label measurements / post processing of parametric maps
  * minimum / mean / maximum / standard deviation intensity maps
  * minimum / mean / maximum / standard deviation of touching / n-nearest / neighbors
* neighbor meshes
  * touching neighbors
  * n-nearest neighbors
  * proximal neighbors
  * distance meshes
* measurements based on label images
  * bounding box 2D / 3D
  * minimum / mean / maximum / sum / standard deviation intensity
  * mass center
  * centroid
  * mean / maximum distance to centroid (and min/max ratio shape descriptor)
  * mean / maximum distance to center of mass (and min/max ratio shape descriptor)
* code export
  * python / Fiji-compatible jython
  * python jupyter notebooks
* pyclesperanto scripting
  * cell counting
  * cell differentiation
  * tissue classification

## Usage
This short tutorial demonstrates how to generate code using the pyclersperanto-assistant. 

<iframe src="https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/pyclesperanto_assistant_screencast.mp4" width="600" height="300"></iframe>
[Download workflow as video](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/pyclesperanto_assistant_screencast.mp4)

### Start up the assistant
Open a command line and start up the assistant and pass the image file you want to process. The shown example image can be found [online](https://github.com/clEsperanto/napari_pyclesperanto_assistant/blob/master/napari_pyclesperanto_assistant/data/CalibZAPWfixed_000154_max-16.tif)

```
python -m napari_pyclesperanto_assistant C:\structure\code\napari_pyclesperanto_assistant\napari_pyclesperanto_assistant\data\CalibZAPWfixed_000154_max-16.tif
```

Alternatively, you can attach the assistant to your napari from within your python code like this:
```python
import napari

# start napari
viewer = napari.Viewer()
viewer.window.add_plugin_dock_widget('clEsperanto')
napari.run()
```

napari will open with the assistant activated:

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_1.png)

### Set up a workflow

Choose categories of operations in the top right panel, for example start with denoising using a Gaussian Blur with sigma 1 in x and y:

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_2.png)

Choose more processing steps. Note: You can change the input image/layer for each operation, the operation and its parameters in the bottom right panel.
For example, continue with these steps
* Filter (Background Removal): Top hat, radius 5 in x and y
* Binarization: Threshold Otsu
* Label: Voronoi labeling 
* Map: Touching neighbor count map
* Binarization: Detect label edges, with the result from the second last step as input.

Hide some layers showing intermediate results. Switch the bleinding of the final result layer to "additive" to see through it on the original image.

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_3.png)

### Code generation
In the plugins menu, you find two entries which allow you to export your workflow as Python/Jython code.
![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_4.png)

Export your workflow as Jupyter notebook. Start the notebook from the command line using
```
jupyter notebook my_notebook.ipynb
```
![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_5.png)

Alternatively, export the workflow as Jython/Python script. This script can be executed from the command line like this
```
python my_script.py
```

It can also be executed in Fiji, in case the [CLIJx-assistant is installed](https://clij.github.io/assistant/installation).

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_6.png)

Note: Depeending on which layers were visible while exporting the code, different code is exported. 
Only visible layers are shown. 
Change layer visibility and export the script again. 
If Fiji asks you if it should reload the script file, click on "Reload".

![](https://github.com/haesleinhuepf/pyclesperanto_assistant/raw/master/docs/images/screenshot_7.png)

## For developers

Getting the recent code from github and locally installing it
```
git clone https://github.com/clesperanto/napari_pyclesperanto_assistant.git

pip install -e ./napari_pyclesperanto_assistant
```

Optional: Also install pyclesperantos recent source code from github:
```
git clone https://github.com/clEsperanto/pyclesperanto_prototype.git

pip install -e ./pyclesperanto_prototype
```

Starting up napari with the pyclesperanto assistant installed:
```
ipython --gui=qt napari_pyclesperanto_assistant\napari_pyclesperanto_assistant
```


## Feedback welcome!
clEsperanto is developed in the open because we believe in the open source community. See our [community guidelines](https://clij.github.io/clij2-docs/community_guidelines). Feel free to drop feedback as [github issue](https://github.com/clEsperanto/pyclesperanto_prototype/issues) or via [image.sc](https://image.sc)

[Imprint](https://clesperanto.github.io/imprint)
