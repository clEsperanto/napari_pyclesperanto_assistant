import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napari_pyclesperanto_assistant",
    version="0.2.0",
    author="haesleinhuepf",
    author_email="robert.haase@tu-dresden.de",
    description="OpenCL based GPU-accelerated image processing in napari",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clesperanto/napari_pyclesperanto_assistant",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "pyopencl", "toolz", "scikit-image", "napari", "napari_plugin_engine", "pyclesperanto_prototype==0.6.0", "magicgui", "numpy==1.19.3"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: napari",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={
        'napari.plugin': [
            'pyclesperanto = napari_pyclesperanto_assistant',
        ],
    },
)
