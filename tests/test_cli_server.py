# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from ssdpy.cli import server as server_cli


def test_invalid_arguments():
    with pytest.raises(SystemExit):
        server_cli.parse_args(("TestServer", "--invalid-argument"))


def test_version():
    with pytest.raises(SystemExit):
        server_cli.parse_args(("TestServer", "--version"))


def test_verbose():
    args = server_cli.parse_args(("TestServer", "-v"))
    assert args.verbose is True

    args = server_cli.parse_args(("TestServer", "--verbose"))
    assert args.verbose is True


def test_ssdpserver_init(mocker):
    mocker.patch.object(server_cli, "SSDPServer")
    server_cli.main(("TestServer",))
    server_cli.SSDPServer.assert_called_once_with(
        "TestServer",
        address=None,
        al=None,
        device_type="ssdp:rootdevice",
        iface=None,
        location=None,
        max_age=None,
        port=1900,
        proto="ipv4",
    )


def test_ssdpserver_init_with_ipv6(mocker):
    mocker.patch.object(server_cli, "SSDPServer")
    server_cli.main(("TestServer", "-6"))
    server_cli.SSDPServer.assert_called_once_with(
        "TestServer",
        address=None,
        al=None,
        device_type="ssdp:rootdevice",
        iface=None,
        location=None,
        max_age=None,
        port=1900,
        proto="ipv6",
    )

    mocker.patch.object(server_cli, "SSDPServer")
    server_cli.main(("TestServer", "--ipv6"))
    server_cli.SSDPServer.assert_called_once_with(
        "TestServer",
        address=None,
        al=None,
        device_type="ssdp:rootdevice",
        iface=None,
        location=None,
        max_age=None,
        port=1900,
        proto="ipv6",
    )


def test_ssdpserver_init_with_args(mocker):
    mocker.patch.object(server_cli, "SSDPServer")
    server_cli.main(
        (
            "TestServer",
            "-i",
            "lo",
            "-a",
            "test-address",
            "-l",
            "test-location",
            "-p",
            "0",
            "-6",
            "-t",
            "test-device",
            "--max-age",
            "0",
        )
    )
    server_cli.SSDPServer.assert_called_once_with(
        "TestServer",
        address="test-address",
        al="test-location",
        device_type="test-device",
        iface=b"lo",
        location="test-location",
        max_age=0,
        port=0,
        proto="ipv6",
    )
