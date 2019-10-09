import unittest
from ssdpy.http_helper import parse_headers


class TestHTTPHelper(unittest.TestCase):

    def test_parse_headers(self):
        good_response = (
            b"HTTP/1.1 200 OK\r\n"
            b"MX: 5\r\n"
        )
        headers = parse_headers(good_response)
        self.assertEqual("5", headers.get("mx"))
        self.assertEqual(None, headers.get("should-not-exist"))

        bad_response = b"not an http response"
        with self.assertRaises(ValueError):
            parse_headers(bad_response)

        another_bad_response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Header: OK\r\n"
            b"Another-header-not-ok\r\n"
        )
        with self.assertRaises(ValueError):
            parse_headers(another_bad_response)
