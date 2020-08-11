.. currentmodule:: ssdpy

======================
Command Line Interface
======================

SSDPy bundles two scripts - ``ssdpy-server`` and ``ssdpy-discover``. These can be used
to interact with SSDP without writing a single line of code.

SSDP Discovery
==============

The ``ssdpy-discover`` command sends SSDP ``DISCOVER`` packets, listens for responses,
and prints the result.

To search for all available services, use the ``ssdp:all`` target:

.. code-block:: sh

    $ ssdpy-discover ssdp:all
