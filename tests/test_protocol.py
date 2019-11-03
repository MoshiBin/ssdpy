# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from ssdpy.protocol import create_msearch_payload, create_notify_payload
from ssdpy.http_helper import parse_headers


class TestProtocol(unittest.TestCase):
    def test_msearch_payload(self):
        data = create_msearch_payload("239.255.255.250:1900", "ssdp:all", mx=1)
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("st"), "ssdp:all")
        self.assertEqual(data_headers.get("man"), '"ssdp:discover"')
        self.assertEqual(data_headers.get("mx"), "1")

    def test_notify_payload(self):
        data = create_notify_payload("239.255.255.250:1900", "testdevice", "ssdpy-test")
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("nt"), "testdevice")
        self.assertEqual(data_headers.get("usn"), "ssdpy-test")
        self.assertIsNone(data_headers.get("non-existant-header"))

    def test_notify_location(self):
        data = create_notify_payload(
            "239.255.255.250:1900",
            "testdevice",
            "ssdpy-test",
            location="http://localhost",
        )
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("nt"), "testdevice")
        self.assertEqual(data_headers.get("usn"), "ssdpy-test")
        self.assertIsNone(data_headers.get("non-existant-header"))
        self.assertEqual(data_headers.get("location"), "http://localhost")

    def test_notify_al(self):
        data = create_notify_payload(
            "239.255.255.250:1900", "testdevice", "ssdpy-test", al="http://localhost"
        )
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("nt"), "testdevice")
        self.assertEqual(data_headers.get("usn"), "ssdpy-test")
        self.assertIsNone(data_headers.get("non-existant-header"))
        self.assertEqual(data_headers.get("al"), "http://localhost")

    def test_notify_age(self):
        data = create_notify_payload(
            "239.255.255.250:1900", "testdevice", "ssdpy-test", max_age=999
        )
        data_headers = parse_headers(data)
        self.assertEqual(data_headers.get("host"), "239.255.255.250:1900")
        self.assertEqual(data_headers.get("nt"), "testdevice")
        self.assertEqual(data_headers.get("usn"), "ssdpy-test")
        self.assertIsNone(data_headers.get("non-existant-header"))
        self.assertEqual(data_headers.get("cache-control"), "max-age=999")

    def test_notify_edge_cases(self):
        with self.assertRaises(ValueError):
            create_notify_payload("x", "y", "z", max_age="not-a-number")
