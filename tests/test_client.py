# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import errno
import pytest
from ssdpy import SSDPClient
from ssdpy.client import discover


def test_client_accepts_ipv4():
    SSDPClient(proto="ipv4")


def test_client_accepts_ipv6():
    SSDPClient(proto="ipv6")


def test_client_rejects_bad_proto():
    with pytest.raises(ValueError):
        SSDPClient(proto="invalid")


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Not all development environments have a predictable loopback device name",
)
def test_client_binds_iface():
    SSDPClient(iface=b"lo")


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="IPv6 testing is broken in GitHub Actions, see https://github.com/actions/virtual-environments/issues/668",
)
def test_client_bind_iface_ipv6():
    try:
        SSDPClient(proto="ipv6", iface=b"lo")
    except OSError as e:
        if e.errno != errno.ENOPROTOOPT:  # Protocol not supported
            raise


def test_client_bind_address_ipv4():
    SSDPClient(address="127.0.0.1")


def test_discover():
    discover()
