# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import signal
import os
import time
from ssdpy.compat import WINDOWS
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
        extra_fields=None,
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
        extra_fields=None,
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
        extra_fields=None,
    )


def test_ssdpserver_init_with_args(mocker):
    mocker.patch.object(server_cli, "SSDPServer")
    server_cli.main(
        (
            "TestServer",
            "-v",
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
            "-e",
            "test-field",
            "foo"
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
        extra_fields={"test-field": "foo"},
    )


@pytest.mark.skipif(WINDOWS or os.environ.get("CI") == "true", reason="No fork() on Windows")
def test_server_keyboard_interrupt():
    pid = os.fork()
    if pid == 0:
        server_cli.main(["TestServer"])
    else:
        time.sleep(2)
        os.kill(pid, signal.SIGINT)
