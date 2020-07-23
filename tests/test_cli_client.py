# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import json
from ssdpy.cli import client as client_cli


def test_client_cli_invalid_arguments():
    with pytest.raises(SystemExit):
        client_cli.parse_args(("--invalid-argument", ))


def test_version():
    with pytest.raises(SystemExit):
        client_cli.parse_args(("--version", ))


def test_verbose():
    args = client_cli.parse_args(("ssdp:test", "-v"))
    assert args.verbose is True

    args = client_cli.parse_args(("ssdp:test", "--verbose"))
    assert args.verbose is True


def test_no_st():
    with pytest.raises(SystemExit):
        client_cli.parse_args((""))


def test_basic_discovery(mocker):
    mocker.patch.object(client_cli, "SSDPClient")
    client_cli.main(("ssdp:test", ))
    client_cli.SSDPClient.assert_called_once_with(
        proto="ipv4",
        port=1900,
        ttl=2,
        iface=None,
        timeout=5,
        address=None,
    )
    # TODO: Check that client.m_search has been called.


def test_client_discovery_ipv6(mocker):
    mocker.patch.object(client_cli, "SSDPClient")
    client_cli.main(("ssdp:test", "--ipv6"))
    client_cli.SSDPClient.assert_called_once_with(
        proto="ipv6",
        port=1900,
        ttl=2,
        iface=None,
        timeout=5,
        address=None,
    )

    mocker.patch.object(client_cli, "SSDPClient")
    client_cli.main(("ssdp:test", "-6"))
    client_cli.SSDPClient.assert_called_once_with(
        proto="ipv6",
        port=1900,
        ttl=2,
        iface=None,
        timeout=5,
        address=None,
    )


def test_client_discovery_all_args(mocker):
    mocker.patch.object(client_cli, "SSDPClient")
    client_cli.main(
        (
            "ssdp:test",
            "-v",
            "-6",
            "-t",
            "100",
            "-o",
            "200",
            "-i",
            "test_iface",
            "-p",
            "0",
            "-m",
            "5",
        )
    )
    client_cli.SSDPClient.assert_called_once_with(
        proto="ipv6",
        port=0,
        ttl=100,
        iface=b"test_iface",
        timeout=200,
        address=None,
    )


def test_client_json_output(capsys):
    client_cli.main(
        ("ssdp:all", "-j")
    )
    output = capsys.readouterr()
    json.loads(output.out)
