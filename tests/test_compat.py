# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import sys
from .compat import PY2
from ssdpy.compat import if_nametoindex


@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_if_nametoindex_none():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(None)


@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_if_nametoindex_int():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(0)


@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_if_nametoindex_nodevice():
    with pytest.raises(OSError):
        if_nametoindex("does-not-exist")


@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_if_nametoindex():
    assert type(if_nametoindex(b"lo")) is int
