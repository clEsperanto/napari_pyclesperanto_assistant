# napari-pyclesperanto-assistant
[![Image.sc forum](https://img.shields.io/badge/dynamic/json.svg?label=forum&url=https%3A%2F%2Fforum.image.sc%2Ftag%2Fclesperanto.json&query=%24.topic_list.tags.0.topic_count&colorB=brightgreen&suffix=%20topics&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAABPklEQVR42m3SyyqFURTA8Y2BER0TDyExZ+aSPIKUlPIITFzKeQWXwhBlQrmFgUzMMFLKZeguBu5y+//17dP3nc5vuPdee6299gohUYYaDGOyyACq4JmQVoFujOMR77hNfOAGM+hBOQqB9TjHD36xhAa04RCuuXeKOvwHVWIKL9jCK2bRiV284QgL8MwEjAneeo9VNOEaBhzALGtoRy02cIcWhE34jj5YxgW+E5Z4iTPkMYpPLCNY3hdOYEfNbKYdmNngZ1jyEzw7h7AIb3fRTQ95OAZ6yQpGYHMMtOTgouktYwxuXsHgWLLl+4x++Kx1FJrjLTagA77bTPvYgw1rRqY56e+w7GNYsqX6JfPwi7aR+Y5SA+BXtKIRfkfJAYgj14tpOF6+I46c4/cAM3UhM3JxyKsxiOIhH0IO6SH/A1Kb1WBeUjbkAAAAAElFTkSuQmCC)](https://forum.image.sc/tag/clesperanto)
[![website](https://img.shields.io/website?url=http%3A%2F%2Fclesperanto.net)](http://clesperanto.net)
[![License](https://img.shields.io/pypi/l/napari-pyclesperanto-assistant.svg?color=green)](https://github.com/clesperanto/napari-pyclesperanto-assistant/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-pyclesperanto-assistant.svg?color=green)](https://pypi.org/project/napari-pyclesperanto-assistant)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-pyclesperanto-assistant.svg?color=green)](https://python.org)
[![tests](https://github.com/clesperanto/napari_pyclesperanto_assistant/workflows/tests/badge.svg)](https://github.com/clesperanto/napari_pyclesperanto_assistant/actions)
[![codecov](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/clesperanto/napari_pyclesperanto_assistant)
[![Development Status](https://img.shields.io/pypi/status/napari_pyclesperanto_assistant.svg)](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-pyclesperanto-assistant)](https://napari-hub.org/plugins/napari-pyclesperanto-assistant)
[![DOI](https://zenodo.org/badge/322312181.svg)](https://zenodo.org/badge/latestdoi/322312181)

The py-clEsperanto-assistant is a yet experimental [napari](https://github.com/napari/napari) plugin for building GPU-accelerated image processing workflows. 
It is part of the [clEsperanto](http://clesperanto.net) project and thus, aims at removing programming language related barriers between image processing ecosystems in the life sciences. 
It uses [pyclesperanto](https://github.com/clEsperanto/pyclesperanto_prototype) and with that [pyopencl](https://documen.tician.de/pyopencl/) as backend for processing images.

This napari plugin adds some menu entries to the Tools menu. You can recognize them with their suffix `(clEsperanto)` in brackets.
Furthermore, it can be used from the [napari-assistant](https://www.napari-hub.org/plugins/napari-assistant) graphical user interface. 
Therefore, just click the menu `Tools > Utilities > Assistant (na)` or run `naparia` from the command line.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/virtual_4d_support1.gif)

## Usage

### Start up the assistant
Start up napari, e.g. from the command line:
```
napari
```

Load example data, e.g. from the menu `File > Open Samples > clEsperanto > CalibZAPWfixed` and 
start the assistant from the menu `Tools > Utilities > Assistant (na)`.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/screenshot1.png)

In case of two dimensional timelapse data, an initial conversion step might be necessary depending on your data source. 
Click the menu `Tools > Utilities > Convert to 2d timelapse`. In the dialog, select the dataset and click ok. 
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

### Neighbor statistics

When working with 2D or 3D data you can analyze measurements in relationship with their neighbors. 
For example, you can measure the area of blobs as shown in the example shown below using the menu 
`Tools > Measurements > Statistics of labeled pixels (clesperant)` and visualize it as `area` image by double-clicking on the table column (1).
Additionally, you can measure the maximum area of the 6 nearest neighbors using the menu `Tools > Measurments > Neighborhood statistics of measurements`.
The new column will then be called "max_nn6_area..." (2). When visualizing such parametric images next by each other, it is recommended to use
[napari-brightness-contrast](https://www.napari-hub.org/plugins/napari-brightness-contrast) and visualize the same intensity range to see differences correctly.

![](https://github.com/clEsperanto/napari_pyclesperanto_assistant/raw/master/docs/images/neighbor_statistics.png)

### Code generation
You can also export your workflow as Python/Jython code or as notebook. See the [napari-assistant documentation](https://www.napari-hub.org/plugins/napari-assistant) for details.

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
  * statistics of neighbors (See related [publication](https://www.frontiersin.org/articles/10.3389/fcomp.2021.774396/full))
* code export
  * python / Fiji-compatible jython
  * python jupyter notebooks
* pyclesperanto scripting
  * cell segmentation
  * cell counting
  * cell differentiation
  * tissue classification

## Installation

It is recommended to install the assistant using mamba. If you have never used mamba before, it is recommended to read 
[this blog post](https://biapol.github.io/blog/mara_lampert/getting_started_with_mambaforge_and_python/readme.html) first. 

```shell
mamba create --name cle_39 python=3.9 napari-pyclesperanto-assistant -c conda-forge
mamba activate cle_39
```

Mac-users please also install this:

    mamba install -c conda-forge ocl_icd_wrapper_apple
    
Linux users please also install this:
    
    mamba install -c conda-forge ocl-icd-system

You can then start the napari-assistant using this command:

```
naparia
```


## Feedback and contributions welcome!
clEsperanto is developed in the open because we believe in the open source community. See our [community guidelines](https://clij.github.io/clij2-docs/community_guidelines). Feel free to drop feedback as [github issue](https://github.com/clEsperanto/pyclesperanto_prototype/issues) or via [image.sc](https://image.sc)

## Acknowledgements
This project was supported by the Deutsche Forschungsgemeinschaft under Germany’s Excellence Strategy – EXC2068 - Cluster of Excellence "Physics of Life" of TU Dresden.
This project has been made possible in part by grant number [2021-240341 (Napari plugin accelerator grant)](https://chanzuckerberg.com/science/programs-resources/imaging/napari/improving-image-processing/) from the Chan Zuckerberg Initiative DAF, an advised fund of the Silicon Valley Community Foundation.

[Imprint](https://clesperanto.github.io/imprint)

