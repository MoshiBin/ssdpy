# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import threading
import time
import pytest
import errno
import os
from ssdpy import SSDPServer


def test_server_ipv4():
    server = SSDPServer("test-server", proto="ipv4")
    server.sock.settimeout(5)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    time.sleep(0.5)
    server.stopped = True
    server_thread.join()


@pytest.mark.skipif(
    os.environ.get("TRAVIS") == "true",
    reason="IPv6 testing is broken in Travis-CI, see https://github.com/travis-ci/travis-ci/issues/8361",
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
    os.environ.get("TRAVIS") != "true",
    reason="Not all development environments have a predictable loopback device name",
)
def test_server_binds_iface():
    SSDPServer("test-server", iface=b"lo")


def test_server_bind_address_ipv4():
    SSDPServer("test-server", address="127.0.0.1")


@pytest.mark.skipif(
    os.environ.get("TRAVIS") == "true",
    reason="IPv6 testing is broken in Travis-CI, see https://github.com/travis-ci/travis-ci/issues/8361",
)
def test_server_bind_address_ipv6():
    SSDPServer("test-server", address="::1", proto="ipv6")


@pytest.mark.skipif(
    os.environ.get("TRAVIS") == "true",
    reason="IPv6 testing is broken in Travis-CI, see https://github.com/travis-ci/travis-ci/issues/8361",
)
def test_server_bind_address_and_iface_ipv6():
    try:
        SSDPServer("test-server", address="::1", proto="ipv6", iface=b"lo")
    except OSError as e:
        if e.errno != errno.ENOPROTOOPT:  # Protocol not supported
            raise
