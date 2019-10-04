# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from six import BytesIO
from six.moves import http_client


class FakeSocket:
    """
    Implements a fake socket from a given response string.
    Used to instantiate http_client.HTTPResponse, which expects a socket-like object.
    """

    def __init__(self, response):
        self._file = BytesIO(response)

    def makefile(self, *args, **kwargs):
        return self._file


def parse_headers(response):
    """
    Receives an HTTP response string and parses the HTTP headers.
    Return a dict of all headers.
    """
    wrapped_response = FakeSocket(response)
    http_response = http_client.HTTPResponse(wrapped_response)
    http_response.begin()
    return dict(http_response.headers)
