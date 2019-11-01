.. ssdpy documentation master file, created by
   sphinx-quickstart on Sat Nov  2 00:11:39 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ssdpy
=====

ssdpy is a lightweight implementation of `SSDP <https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol>`_ (Simple Service Discovery Protocol). It is designed for ease of use and high compatibility with the protocol in real-life use. It supports both the IETF and UPnP versions of the protocol.

It's easy to search for services:

    from ssdpy import SSDPClient
    client = SSDPClient()
    client.m_search("ssdp:all")

Features
--------

- SSDP client with M-Search capabilities.
- SSDP server with Notify and the ability to serve forever.
- Supports Python 2.7 and 3.
- Lightweight and tolerant of different SSDP versions (IETF, UPnP v1+v2).
- Fully supports IPv6.

Installation
------------

Install ssdpy by running:

    pip install ssdpy

Contribute
----------

- Issue Tracker: github.com/MoshiBin/ssdpy/issues
- Source Code: github.com/MoshiBin/ssdpy

License
-------

This project is licensed under the MIT license.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
