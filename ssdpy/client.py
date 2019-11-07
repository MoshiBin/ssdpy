# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import socket
from .constants import IPv4, IPv6, ipv4_multicast_ip, ipv6_multicast_ip
from .http_helper import parse_headers
from .protocol import create_msearch_payload


class SSDPClient(object):
    def __init__(
        self, proto=IPv4, port=1900, ttl=2, iface=None, timeout=5, *args, **kwargs
    ):
        allowed_protos = (IPv4, IPv6)
        if proto not in allowed_protos:
            raise ValueError(
                "Invalid proto - expected one of {}".format(allowed_protos)
            )
        self.port = port
        if proto is IPv4:
            af_type = socket.AF_INET
            self.broadcast_ip = ipv4_multicast_ip
            self._address = (self.broadcast_ip, port)
        elif proto is IPv6:
            af_type = socket.AF_INET6
            self.broadcast_ip = ipv6_multicast_ip  # TODO: Support other ipv6 multicasts
            self._address = (self.broadcast_ip, port, 0, 0)
        self.sock = socket.socket(af_type, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.sock.settimeout(timeout)
        if iface is not None:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, iface)

    def send(self, data):
        self.sock.sendto(data, self._address)

    def recv(self):
        try:
            while True:
                data = self.sock.recv(1024)
                yield data
        except socket.timeout:
            pass
        return

    def m_search(self, st="ssdp:all", mx=1):
        """
        Send an M-SEARCH request and gather responses.

        Parameters
        ----------
        st : str
            The Search Target, used to narrow down the responses
            that should be received. Defaults to "ssdp:all" which should get
            responses from any SSDP-enabled device.

        mx : int
            Maximum wait time (in seconds) that devices are allowed to wait before
            sending a response. Should be between 1 and 5, though this is not enforced
            in this implementation.
            Devices will randomly wait for anywhere between 0 and 'mx' seconds in
            order to avoid flooding the client that sends the M-SEARCH. Increase the
            value of 'mx' if you expect a large number of devices to answer, in order
            to avoid losing responses.
        """
        host = "{}:{}".format(self.broadcast_ip, self.port)
        data = create_msearch_payload(host, st, mx)
        self.send(data)
        responses = [x for x in self.recv()]
        parsed_responses = []
        for response in responses:
            try:
                headers = parse_headers(response)
                parsed_responses.append(headers)
            except ValueError:
                # Invalid response, do nothing.
                # TODO: Log dropped responses
                pass
        return parsed_responses


def discover():
    ms = SSDPClient()
    responses = ms.m_search()
    ret = []
    for response in responses:
        headers = parse_headers(response)
        ret.append(headers)
    return ret
