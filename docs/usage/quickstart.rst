==========
Quickstart
==========

Run SSDP discovery from shell
=============================


.. note:: SSDP works by sending and receiving multicasts. This sometimes requires
          elevated permissions. If you get an error trying to use these commands, try
          running them as ``root`` (for example, using ``sudo``).

Discover services using SSDP
----------------------------
Searching for the special service type ``ssdp:all`` should return answers from all
active services.

.. code-block:: sh

    $ ssdpy-discover ssdp:all

Discover a specific type of service
-----------------------------------

Specify a different service type to only get responses from relevant services. For
example, if we want to find all `DIAL`_ services (e.g. Chromecast devices):

.. code-block:: sh

    $ ssdpy-discover urn:dial-multiscreen-org:service:dial:1

.. _DIAL: http://www.dial-multiscreen.org/


Run SSDP Server from shell
==========================

.. code-block:: sh

    $ ssdpy-server my-special-service --location 'http://10.0.0.1:8080/hello'



SSDP Discovery from Python
==========================

:class:`ssdpy.SSDPClient`

.. code-block:: python

    from ssdpy import SSDPClient
    client = SSDPClient()

SSDP Server from Python
=======================

:class:`ssdpy.SSDPServer`

.. code-block:: python

    from ssdpy import SSDPServer
    server = SSDPServer("my-special-service", location="http://192.168.0.100:8080/hello")
    server.serve_forever()
