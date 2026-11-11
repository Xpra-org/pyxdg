#!/usr/bin/env python3

from setuptools import setup

setup(
    name="pyxdg",
    version="0.29",
    description="PyXDG contains implementations of freedesktop.org standards in python.",
    maintainer="Antoine Martin",
    maintainer_email="totaam@xpra.org",
    url="https://github.com/Xpra-org/pyxdg",
    packages=["xdg"],
    python_requires=">=3.10",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Desktop Environment",
    ],
)
