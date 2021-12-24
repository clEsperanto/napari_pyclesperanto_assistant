#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from pathlib import Path

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
root = Path(__file__).parent
filename = str(root / "requirements.txt")
with open(filename) as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)


# https://github.com/pypa/setuptools_scm
#use_scm = {"write_to": "napari_pyclesperanto_assistant/_version.py"}
setup(
    name="napari_pyclesperanto_assistant",
    version="0.11.8",
    author="Robert Haase, Talley Lambert",
    author_email="robert.haase@tu-dresden.de",
    description="GPU-accelerated image processing in napari using OpenCL",
    license="BSD-3-Clause",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clesperanto/napari_pyclesperanto_assistant",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requirements,
    #use_scm_version=use_scm,
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: napari",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={
        "napari.plugin": [
            "clEsperanto = napari_pyclesperanto_assistant._napari_plugin",
        ],
    },
)
