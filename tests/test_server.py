# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import threading
import time
import pytest
import errno
import os
import sys
from ssdpy import SSDPServer
from ssdpy.compat import LINUX


def test_server_ipv4():
    server = SSDPServer("test-server", proto="ipv4")
    server.sock.settimeout(5)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    time.sleep(0.5)
    server.stopped = True
    server_thread.join()


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="IPv6 testing is broken in GitHub Actions, see https://github.com/actions/virtual-environments/issues/668",
)
def test_server_ipv6():
    server = SSDPServer("test-server-ipv6", proto="ipv6")
    server.sock.settimeout(5)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    time.sleep(0.5)
    server.stopped = True
    server_thread.join()


def test_server_invalid_proto():
    with pytest.raises(ValueError):
        SSDPServer("test-server", proto="invalid")


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Not all development environments have a predictable loopback device name",
)
@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_server_binds_iface():
    SSDPServer("test-server", iface=b"lo")


def test_server_bind_address_ipv4():
    SSDPServer("test-server", address="127.0.0.1")


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="IPv6 testing is broken in GitHub Actions, see https://github.com/actions/virtual-environments/issues/668",
)
def test_server_bind_address_ipv6():
    SSDPServer("test-server", address="::1", proto="ipv6")


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="IPv6 testing is broken in GitHub Actions, see https://github.com/actions/virtual-environments/issues/668",
)
@pytest.mark.skipif(sys.platform == "win32", reason="No bind to interface on Windows")
def test_server_bind_address_and_iface_ipv6():
    try:
        SSDPServer("test-server", address="::1", proto="ipv6", iface=b"lo")
    except OSError as e:
        if e.errno != errno.ENOPROTOOPT:  # Protocol not supported
            raise


def test_server_extra_fields():
    SSDPServer("test-server", extra_fields={"test-field": "foo", "test-field2": "bar"})


def test_server_extra_fields_non_ascii():
    with pytest.raises(ValueError):
        SSDPServer("test-server", extra_fields={"invalid-field™": "foo"})


@pytest.mark.skipif(LINUX, reason="This limitation only occurs on Windows")
def test_server_bind_interface_in_windows():
    with pytest.raises(ValueError):
        SSDPServer("test-server", iface=b"Ethernet")
