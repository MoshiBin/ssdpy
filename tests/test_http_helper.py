# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from ssdpy.http_helper import parse_headers


def test_parse_headers():
    good_response = b"HTTP/1.1 200 OK\r\n" b"MX: 5\r\n"
    headers = parse_headers(good_response)
    assert headers.get("mx") == "5"


def test_parse_headers_invalid_header():
    good_response = b"HTTP/1.1 200 OK\r\n" b"MX: 5\r\n"
    headers = parse_headers(good_response)
    assert headers.get("should-not-exist") is None


def test_parse_headers_invalid_response():
    bad_response = b"not an http response"
    with pytest.raises(ValueError):
        parse_headers(bad_response)


def test_parse_headers_bad_response_header():
    bad_response = (
        b"HTTP/1.1 200 OK\r\n" b"Header: OK\r\n" b"Another-header-not-ok\r\n"
    )
    with pytest.raises(ValueError):
        parse_headers(bad_response)


def test_empty_response():
    empty_response = b"HTTP/1.1 200 OK\r\n"
    parse_headers(empty_response)
