# To make this script run in cpython, install pyclesperanto_prototype:
# pip install pyclesperanto_prototype
# Read more: 
# https://clesperanto.net
# 
# To make this script run in Fiji, please activate the clij, # clij2 and clijx-assistant update sites in your Fiji. 
# Read more: 
# https://clij.github.io/assistant
# 
# Generator (P) version: 0.1.0
# 
import pyclesperanto_prototype as cle

image0 = cle.imread('C:/structure/code/napari_pyclesperanto_assistant/napari_pyclesperanto_assistant/data/CalibZAPWfixed_000154_max-16.tif')
# show result
cle.imshow(image0, 'image', False, 0.0, 255.0)

# Layer Result of gaussian_blur
image1 = cle.create_like(image0)
cle.gaussian_blur(image0, image1, 1.0, 1.0, 0.0)
# show result
cle.imshow(image1, 'Result of gaussian_blur', False, 0, 254.8003692626953)

# Layer Result of top_hat_box
image2 = cle.create_like(image1)
cle.top_hat_box(image1, image2, 10.0, 10.0, 0.0)
# show result
cle.imshow(image2, 'Result of top_hat_box', False, 0, 237.11058)

# Layer Result of threshold_otsu
image3 = cle.create_like(image2)
cle.threshold_otsu(image2, image3)
# show result
cle.imshow(image3, 'Result of threshold_otsu', False, 0, 1)

# Layer Result of voronoi_labeling
image4 = cle.create_like(image3)
cle.voronoi_labeling(image3, image4)
# show result
cle.imshow(image4, 'Result of voronoi_labeling', True)

# Layer Result of detect_label_edges
image5 = cle.create_like(image4)
cle.detect_label_edges(image4, image5)
# show result
cle.imshow(image5, 'Result of detect_label_edges', False, 0, 1)

