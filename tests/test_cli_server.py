# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from .compat import mock
from ssdpy.cli import server as server_cli


class TestServerCLI(unittest.TestCase):
    def test_invalid_arguments(self):
        with self.assertRaises(SystemExit):
            server_cli.parse_args(("TestServer", "--invalid-argument"))

    def test_version(self):
        with self.assertRaises(SystemExit):
            server_cli.parse_args(("TestServer", "--version"))

    def test_verbose(self):
        args = server_cli.parse_args(("TestServer", "-v"))
        self.assertTrue(args.verbose)

        args = server_cli.parse_args(("TestServer", "--verbose"))
        self.assertTrue(args.verbose)

    def test_ssdpserver_init(self):
        server_cli.SSDPServer = mock.MagicMock()
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

    def test_ssdpserver_init_with_ipv6(self):
        server_cli.SSDPServer = mock.MagicMock()
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

        server_cli.SSDPServer = mock.MagicMock()
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

    def test_ssdpserver_init_with_args(self):
        server_cli.SSDPServer = mock.MagicMock()
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
