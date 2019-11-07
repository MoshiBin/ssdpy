#!/usr/bin/env python

from setuptools import setup, find_packages
from ssdpy.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ssdpy",
    version=VERSION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Python SSDP library",
    license="MIT",
    author="Moshi Binyamini",
    author_email="moshi@moshib.in",
    url="https://github.com/MoshiBin/ssdpy",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=2.7",
    entry_points={
        "console_scripts": [
            "ssdpy-server = ssdpy.cli.server:main",
            "ssdpy-discover = ssdpy.cli.client:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

)
