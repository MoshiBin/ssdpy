# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .version import VERSION
from .server import SSDPServer
from .client import SSDPClient

__version__ = VERSION

__all__ = ["SSDPServer", "SSDPClient"]
