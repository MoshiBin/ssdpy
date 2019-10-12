# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from ssdpy.protocol import create_msearch_payload
from ssdpy.http_helper import parse_headers


class TestProtocol(unittest.TestCase):
    def test_msearch_payload(self):
        data = create_msearch_payload("239.255.255.250:1900", "ssdp:all", mx=1)
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("st"), "ssdp:all")
        self.assertEqual(data_headers.get("man"), "ssdp:discover")
        self.assertEqual(data_headers.get("mx"), "1")
