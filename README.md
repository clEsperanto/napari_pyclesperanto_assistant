# napari-pyclesperanto-assistant
[![Image.sc forum](https://img.shields.io/badge/dynamic/json.svg?label=forum&url=https%3A%2F%2Fforum.image.sc%2Ftag%2Fclesperanto.json&query=%24.topic_list.tags.0.topic_count&colorB=brightgreen&suffix=%20topics&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAABPklEQVR42m3SyyqFURTA8Y2BER0TDyExZ+aSPIKUlPIITFzKeQWXwhBlQrmFgUzMMFLKZeguBu5y+//17dP3nc5vuPdee6299gohUYYaDGOyyACq4JmQVoFujOMR77hNfOAGM+hBOQqB9TjHD36xhAa04RCuuXeKOvwHVWIKL9jCK2bRiV284QgL8MwEjAneeo9VNOEaBhzALGtoRy02cIcWhE34jj5YxgW+E5Z4iTPkMYpPLCNY3hdOYEfNbKYdmNngZ1jyEzw7h7AIb3fRTQ95OAZ6yQpGYHMMtOTgouktYwxuXsHgWLLl+4x++Kx1FJrjLTagA77bTPvYgw1rRqY56e+w7GNYsqX6JfPwi7aR+Y5SA+BXtKIRfkfJAYgj14tpOF6+I46c4/cAM3UhM3JxyKsxiOIhH0IO6SH/A1Kb1WBeUjbkAAAAAElFTkSuQmCC)](https://forum.image.sc/tag/clesperanto)
[![website](https://img.shields.io/website?url=http%3A%2F%2Fclesperanto.net)](http://clesperanto.net)
[![License](https://img.shields.io/pypi/l/napari-pyclesperanto-assistant.svg?color=green)](https://github.com/clesperanto/napari-pyclesperanto-assistant/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-pyclesperanto-assistant.svg?color=green)](https://pypi.org/project/napari-pyclesperanto-assistant)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-pyclesperanto-assistant.svg?color=green)](https://python.org)
[![tests](https://github.com/clesperanto/napari_pyclesperanto_assistant/workflows/tests/badge.svg)](https://github.com/clesperanto/napari_pyclesperanto_assistant/actions)
[![codecov](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant)

The py-clEsperanto-assistant is a yet experimental [napari](https://github.com/napari/napari) plugin for building GPU-accelerated image processing workflows. 
It is part of the [clEsperanto](http://clesperanto.net) project and thus, aims at removing programming language related barriers between image processing ecosystems in the life sciences. 
It uses [pyclesperanto](https://github.com/clEsperanto/pyclesperanto_prototype) and with that [pyopencl](https://documen.tician.de/pyopencl/) as backend for processing images.
This plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) using with napari's [cookiecutter-napari-plugin](https://github.com/napari/cookiecutter-napari-plugin) template.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/virtual_4d_support1.gif)

## Installation

It is recommended to install the assistant via conda:
```shell
conda create --name bio11 python==3.8.5 
conda activate bio11 
conda install -c conda-forge pyopencl
pip install napari-pyclesperanto-assistant
pip install "napari[all]"
```

Alternatively, you can install the assistant using napari's plugin installer in the menu `Plugins > Install/uninstall Packages`.
Windows users should paste this URL

```
https://github.com/clEsperanto/napari_pyclesperanto_assistant/blob/master/installation_help/pyopencl-2020.3.1+cl12-cp38-cp38-win_amd64.whl?raw=true
```

in this field and click on `Install` before proceeding:
![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot_installer2.png)

Afterwards, click install clEsperanto like by clicking on `Install` here:

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot_installer.png)

You can then start napari, e.g. from command line, and find the assistant in the `Plugins` menu.
```shell
napari
```

Also consider installing napari-workflow-inspector for visualizing the workflows you build using the assistant:

```
pip install napari-workflow-inspector
```

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/workflow_inspector.gif)

## Features
[pyclesperanto](https://github.com/clEsperanto/pyclesperanto_prototype) offers various possibilities for processing images. It comes from developers who work in life sciences and thus, it may be focused towards processing two- and three-dimensional microscopy image data showing cells and tissues. A selection of pyclesperanto's functionality is available via the assistant user interface. Typical workflows which can be built with this assistant include
* image filtering
  * denoising / noise reduction (mean, median, Gaussian blur)
  * background subtraction for uneven illumination or out-of-focus light (bottom-hat, top-hat, subtract Gaussian background)
  * grey value morphology (local minimum, maximum. variance)
  * gamma correction
  * Laplace operator
  * Sobel operator
* combining images
  * masking
  * image math (adding, subtracting, multiplying, dividing images) 
  * absolute / squared difference
* image transformations
  * translation
  * rotation
  * scale
  * reduce stack  
  * sub-stacks
* image projections
  * minimum / mean / maximum / sum / standard deviation projections
* image segmentation
  * binarization (thresholding, local maxima detection)
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
  * extend labels via Voronoi
  * exclude labels on edges
  * exclude labels within / out of size / value range
  * merge touching labels
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
  * center of mass
  * centroid
  * mean / maximum distance to centroid (and extension ratio shape descriptor)
  * mean / maximum distance to center of mass (and extension ratio shape descriptor)
* code export
  * python / Fiji-compatible jython
  * python jupyter notebooks
* pyclesperanto scripting
  * cell segmentation
  * cell counting
  * cell differentiation
  * tissue classification

## Usage

### Start up the assistant
Start up napari, e.g. from the command line:
```
napari
```

Load example data, e.g. from the menu `File > Open Samples > clEsperanto > CalibZAPWfixed` and 
start the assistant from the menu `Plugins > clEsperanto > Assistant`. Select a GPU in case you are asked to.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot1.png)

In case of two dimensional timelapse data, an initial conversion step might be necessary depending on your data source. 
Click the menu `Plugins > clEsperanto > Convert to 2d timelapse`. In the dialog, select the dataset and click ok. 
You can delete the original dataset afterwards:

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot1a.png)

### Set up a workflow

Choose categories of operations in the top right panel, for example start with denoising using a Gaussian Blur with sigma 1 in x and y.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot2.png)

Continue with background removal using the top-hat filter with radius 5 in x and y.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot2a.png)

For labeling the objects, use [Voronoi-Otsu-Labeling](https://nbviewer.jupyter.org/github/clEsperanto/pyclesperanto_prototype/blob/master/demo/segmentation/voronoi_otsu_labeling.ipynb) with both sigma parameters set to 2.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot2b.png)

The labeled objects can be extended using a Voronoi diagram to derive a estimations of cell boundaries.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot2c.png)

You can then configure napari to show the label boundaries on top of the original image:

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot2d.png)

When your workflow is set up, click the play button below your dataset:

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/timelapse_2d.gif)

### Code generation
You can also export your workflow as Python/Jython code or as notebook.
![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot3.png)

After exporting your workflow as Jupyter notebook, you can start the notebook from the command line using
```
jupyter notebook my_notebook.ipynb
```

In some cases you need to replace the command `cle.imread('None`)` with a command loading your image data. 
After that, you can execute the notebook.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/notebook.png)

You can also export code to the clipboard or as python code to disc. 
This python code can also be executed in [Fiji](https://fiji.sc)`s Jython, in case the [CLIJx-assistant is installed](https://clij.github.io/assistant/installation).

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/fiji_execution.png)

Alternatively, you can also generate code and edit it directly in the Script Editor. 
Therefore, the [napari-script-editor](https://www.napari-hub.org/plugins/napari-script-editor) must be installed.

![img.png](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/script_editor.png)

Also note: The generated python/jython code is not capable of processing timelapse data,
you need to program a for-loop processing timepoints individually yourself. 
See also [this notebook](https://github.com/BiAPoL/Bio-image_Analysis_with_Python/blob/main/image_processing/12_process_folders.ipynb) for how to do this.

Work in progress, contributions welcome.

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

## Feedback welcome!
clEsperanto is developed in the open because we believe in the open source community. See our [community guidelines](https://clij.github.io/clij2-docs/community_guidelines). Feel free to drop feedback as [github issue](https://github.com/clEsperanto/pyclesperanto_prototype/issues) or via [image.sc](https://image.sc)

[Imprint](https://clesperanto.github.io/imprint)
