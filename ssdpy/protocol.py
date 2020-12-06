# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def create_msearch_payload(host, st, mx=1):
    """
    Create an M-SEARCH packet using the given parameters.
    Returns a bytes object containing a valid M-SEARCH request.

    :param host: The address (IP + port) that the M-SEARCH will be sent to. This is usually a multicast address.
    :type host: str

    :param st: Search target. The type of services that should respond to the search.
    :type st: str

    :param mx: Maximum wait time, in seconds, for responses.
    :type mx: int

    :return: A bytes object containing the generated M-SEARCH payload.
    """
    data = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST:{}\r\n"
        'MAN: "ssdp:discover"\r\n'
        "ST:{}\r\n"
        "MX:{}\r\n"
        "\r\n"
    ).format(host, st, mx)
    return data.encode("utf-8")


def create_notify_payload(host, nt, usn, location=None, al=None, max_age=None, extra_fields=None):
    """
    Create a NOTIFY packet using the given parameters.
    Returns a bytes object containing a valid NOTIFY request.

    The NOTIFY request is different between IETF SSDP and UPnP SSDP.
    In IETF, the 'location' and 'al' fields serve the same purpose, and can be
    provided together (if so, they should point to the same location) or not at
    all.
    In UPnP, the 'location' field MUST be provided, and 'al' is ignored.
    Sending both 'location' and 'al' is the more widely supported option. It
    does not, however, mean that all SSDP implementations would accept a packet
    with both. Therefore the option to send just one of these fields (or none at
    all) is supported.
    If in doubt, send both. If your notifications go ignored, opt to not send 'al'.

    :param host:  The address (IP + port) that the NOTIFY will be sent about. This is usually a multicast address.
    :type host: str

    :param nt: Notification type. Indicates which device is sending the notification.
    :type nt: str

    :param usn: Unique identifier for the service. Usually this will be composed of a UUID or any other universal identifier.
    :type usn: str

    :param location: A URL for more information about the service. This parameter is only valid when sending a UPnP SSDP packet, not IETF.
    :type location: str

    :param al: Similar to 'location', but only supported on IETF SSDP, not UPnP.
    :type al: str

    :param max_age: Amount of time in seconds that the NOTIFY packet should be cached by clients receiving it. In UPnP, this header is required.
    :type max_age: int

    :param extra_fields: Extra header fields to send. UPnP SSDP section 1.1.3 allows for extra vendor-specific fields to be sent in the NOTIFY packet. According to the spec, the field names MUST be in the format of `token`.`domain-name`, for example `myheader.philips.com`. SSDPy, however, does not check this. Normally, headers should be in ASCII - but this function does not enforce that.

    :return: A bytes object containing the generated NOTIFY payload.
    """
    if max_age is not None and not isinstance(max_age, int):
        raise ValueError("max_age must by of type: int")
    data = (
        "NOTIFY * HTTP/1.1\r\n"
        "HOST:{}\r\n"
        "NT:{}\r\n"
        "NTS:ssdp:alive\r\n"
        "USN:{}\r\n"
    ).format(host, nt, usn)
    if location is not None:
        data += "LOCATION:{}\r\n".format(location)
    if al is not None:
        data += "AL:{}\r\n".format(al)
    if max_age is not None:
        data += "Cache-Control:max-age={}\r\n".format(max_age)
    if extra_fields is not None:
        for field, value in extra_fields.items():
            data += "{}:{}\r\n".format(field, value)
    data += "\r\n"
    return data.encode("utf-8")
