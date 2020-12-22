# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import threading
import pytest
from ssdpy import SSDPServer, SSDPClient
from ssdpy.cli import client as client_cli


@pytest.fixture(scope="session", autouse=True)
def ssdpy_server():
    server = SSDPServer("test-server")
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()


def test_system(ssdpy_server):
    """System test: Start a server on localhost, then try to discover the server"""
    client = SSDPClient()
    results = client.m_search()
    assert results
    assert list(filter(lambda response: response.get("usn") == "test-server", results))


def test_system_cli(ssdpy_server):
    client_cli.main(["ssdp:all"])
