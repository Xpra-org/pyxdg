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
    python_requires=">=3.2",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
    ],
)
