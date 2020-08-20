# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from .compat import PY2
from ssdpy.compat import if_nametoindex


def test_if_nametoindex_none():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(None)


def test_if_nametoindex_int():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(0)


def test_if_nametoindex_nodevice():
    with pytest.raises(OSError):
        if_nametoindex("does-not-exist")


def test_if_nametoindex():
    assert type(if_nametoindex(b"lo")) is int
