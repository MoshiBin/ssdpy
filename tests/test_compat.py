# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import sys
import socket
from .compat import PY2
from ssdpy.compat import if_nametoindex, inet_pton, WINDOWS, MACOSX


@pytest.mark.skipif(WINDOWS or MACOSX, reason="No bind to interface on Win32/Mac")
def test_if_nametoindex_none():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(None)


@pytest.mark.skipif(WINDOWS or MACOSX, reason="No bind to interface on Win32/Mac")
def test_if_nametoindex_int():
    if PY2:
        with pytest.raises(TypeError):
            if_nametoindex(0)


@pytest.mark.skipif(WINDOWS or MACOSX, reason="No bind to interface on Win32/Mac")
def test_if_nametoindex_nodevice():
    with pytest.raises(OSError):
        if_nametoindex("does-not-exist")


@pytest.mark.skipif(WINDOWS or MACOSX, reason="No bind to interface on Win32/Mac")
def test_if_nametoindex():
    assert type(if_nametoindex(b"lo")) is int


@pytest.mark.skipif(not (PY2 and WINDOWS), reason="Only test compat inet_pton")
def test_inet_pton():
    assert (
        inet_pton(socket.AF_INET6, "dead::beef") == b"\xde\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbe\xef"
    )


@pytest.mark.skipif(not (PY2 and WINDOWS), reason="Only test compat inet_pton")
def test_inet_pton_bad_addr():
    with pytest.raises(OSError):
        inet_pton(socket.AF_INET6, "bad address")


@pytest.mark.skipif(not (PY2 and WINDOWS), reason="Only test compat inet_pton")
def test_inet_pton_wrong_proto():
    with pytest.raises(ValueError):
        inet_pton(socket.AF_INET, "127.0.0.1")
