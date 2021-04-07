import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
with open('requirements.txt') as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)
setuptools.setup(
    name="napari_pyclesperanto_assistant",
    version="0.7.5",
    author="Robert Haase",
    author_email="robert.haase@tu-dresden.de",
    license='BSD-3',
    description="OpenCL based GPU-accelerated image processing in napari",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clesperanto/napari_pyclesperanto_assistant",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "pyopencl", "toolz", "scikit-image", "napari==0.4.7", "napari_plugin_engine", "pyclesperanto_prototype==0.7.5", "magicgui", "numpy!=1.19.4", "pyperclip"],
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
            'clEsperanto = napari_pyclesperanto_assistant',
        ],
    },
)
