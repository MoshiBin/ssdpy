# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from ssdpy.protocol import create_msearch_payload, create_notify_payload
from ssdpy.http_helper import parse_headers


def test_msearch_payload():
    data = create_msearch_payload("239.255.255.250:1900", "ssdp:all", mx=1)
    data_headers = parse_headers(data)
    assert data_headers.get("host") == "239.255.255.250:1900"
    assert data_headers.get("st") == "ssdp:all"
    assert data_headers.get("man") == '"ssdp:discover"'
    assert data_headers.get("mx") == "1"


def test_notify_payload():
    data = create_notify_payload("239.255.255.250:1900", "testdevice", "ssdpy-test")
    data_headers = parse_headers(data)
    assert data_headers.get("host") == "239.255.255.250:1900"
    assert data_headers.get("nt") == "testdevice"
    assert data_headers.get("usn") == "ssdpy-test"
    assert data_headers.get("non-existant-header") is None


def test_notify_location():
    data = create_notify_payload(
        "239.255.255.250:1900",
        "testdevice",
        "ssdpy-test",
        location="http://localhost",
    )
    data_headers = parse_headers(data)
    assert data_headers.get("host") == "239.255.255.250:1900"
    assert data_headers.get("nt") == "testdevice"
    assert data_headers.get("usn") == "ssdpy-test"
    assert data_headers.get("non-existant-header") is None
    assert data_headers.get("location") == "http://localhost"


def test_notify_al():
    data = create_notify_payload("239.255.255.250:1900", "testdevice", "ssdpy-test", al="http://localhost")
    data_headers = parse_headers(data)
    assert data_headers.get("host") == "239.255.255.250:1900"
    assert data_headers.get("nt") == "testdevice"
    assert data_headers.get("usn") == "ssdpy-test"
    assert data_headers.get("non-existant-header") is None
    assert data_headers.get("al") == "http://localhost"


def test_notify_age():
    data = create_notify_payload("239.255.255.250:1900", "testdevice", "ssdpy-test", max_age=999)
    data_headers = parse_headers(data)
    assert data_headers.get("host") == "239.255.255.250:1900"
    assert data_headers.get("nt") == "testdevice"
    assert data_headers.get("usn") == "ssdpy-test"
    assert data_headers.get("non-existant-header") is None
    assert data_headers.get("cache-control") == "max-age=999"


def test_notify_edge_cases():
    with pytest.raises(ValueError):
        create_notify_payload("x", "y", "z", max_age="not-a-number")


def test_notify_extra_fields():
    data = create_notify_payload(
        "239.255.255.250:1900",
        "testdevice",
        "ssdpy-test",
        extra_fields={"test-header": "test-value", "test-header.domain.com": "test-value2"},
    )
    data_headers = parse_headers(data)
    assert data_headers.get("test-header") == "test-value"
    assert data_headers.get("test-header.domain.com") == "test-value2"
    assert data_headers.get("non-existant-header") is None
