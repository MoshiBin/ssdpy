# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import threading
import time
import unittest
from ssdpy import SSDPServer


class TestProtocol(unittest.TestCase):
    def test_server_ipv4(self):
        server = SSDPServer("test-server", proto="ipv4")
        server.sock.settimeout(5)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        time.sleep(0.5)
        server.stopped = True
        server_thread.join()

    # Skip this test - IPv6 testing is broken for Travis-CI
    # see https://github.com/travis-ci/travis-ci/issues/8361 for more info
    @unittest.SkipTest
    def test_server_ipv6(self):
        server = SSDPServer("test-server-ipv6", proto="ipv6")
        server.sock.settimeout(5)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        time.sleep(0.5)
        server.stopped = True
        server_thread.join()
