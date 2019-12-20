# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import threading
import time
import pytest
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
