#!/usr/bin/env python

from setuptools import setup, find_packages
from ssdpy.version import VERSION

setup(
    name="ssdpy",
    version=VERSION,
    description="Python SSDP library",
    license="MIT",
    author="Moshi Binyamini",
    author_email="moshi@moshib.in",
    url="https://github.com/MoshiBin/ssdpy",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=2.7",
)
