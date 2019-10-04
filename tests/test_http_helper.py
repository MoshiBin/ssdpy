import unittest
from ssdpy.http_helper import FakeSocket, parse_headers


class TestHTTPHelper(unittest.TestCase):
    def test_fake_socket(self):
        with self.assertRaises(TypeError):
            FakeSocket("xxx")
        fs = FakeSocket(b"xxx")
        self.assertIsInstance(fs, FakeSocket)

    def test_parse_headers(self):
        good_response = (
            b"HTTP/1.1 200 OK\r\n"
            b"MX: 5\r\n"
        )
        headers = parse_headers(good_response)
        self.assertEqual("5", headers.get("MX"))
        self.assertEqual(None, headers.get("SHOULD-NOT-EXIST"))

        bad_response = b"not an http response"
        with self.assertRaises(Exception):
            parse_headers(bad_response)
