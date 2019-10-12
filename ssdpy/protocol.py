# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def create_msearch_payload(host, st, mx=1):
    """
    Create an M-SEARCH packet using the given parameters.
    Returns a bytes object containing a valid M-SEARCH request.

    Parameters
    ----------
    host : str
        The address (IP + port) that the M-SEARCH will be sent to.
        This is usually a multicast address.
    st : str

    """
    data = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST:{}\r\n"
        "MAN:ssdp:discover\r\n"
        "ST:{}\r\n"
        "MX:{}\r\n"
    ).format(host, st, mx)
    return data.encode("utf-8")
