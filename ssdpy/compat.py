# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import socket
import sys


PY2 = sys.version_info[0] == 2

string_types = basestring if PY2 else str  # noqa


# Python 2 doesn't have socket.if_nametoindex so we need to implement it manually
if PY2:
    import ctypes
    import ctypes.util

    libc = ctypes.CDLL(ctypes.util.find_library('c'))

    def if_nametoindex(name):
        """
        Return the logical index number of the given interface name.
        """
        if not isinstance(name, string_types):
            raise TypeError("Expected string type, got '{}'".format(type(name)))

        rc = libc.if_nametoindex(name)
        if rc == 0:
            raise OSError("no interface with this name '{}'".format(name))
        return rc
else:
    if_nametoindex = socket.if_nametoindex


SO_BINDTODEVICE = getattr(socket, "SO_BINDTODEVICE", 25)
