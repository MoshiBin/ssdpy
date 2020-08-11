Installation
============

Python Version
--------------

The latest Python 3 version is always recommended, since it has all the latest bells and
whistles. SSDPy supports Python 3.5 and above, and also Python 2.7 for compatibility
with legacy projects.

Dependencies
------------

SSDPy only uses packages from the standard library, so no additional dependencies will
be installed when installing SSDPy. We aim to be as lightweight as possible, so even
`six`_ is not required.

.. _six: https://six.readthedocs.io/

Install SSDPy
-------------

SSDPy is available on `PyPI`_, and can be installed using pip. The version on PyPI is
always the latest stable release.

.. _PyPi: https://pypi.org/project/ssdpy/

.. code-block:: sh

    $ pip install ssdpy

Installing bleeding edge version
********************************

If you want to work with the latest SSDPy code before it's released, install directly
from the master branch. The master branch undergoes constant testing to verify some
level of stability, but issues may happen.

.. code-block:: sh

    $ pip install -U https://github.com/MoshiBin/ssdpy/archive/master.zip
