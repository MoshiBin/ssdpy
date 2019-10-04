# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import socket
from .constants import IPv4, IPv6
from .http_helper import parse_headers


class MulticastSocket(object):
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
            self.broadcast_ip = "239.255.255.250"
            self._address = (self.broadcast_ip, port)
        elif proto is IPv6:
            af_type = socket.AF_INET6
            self.broadcast_ip = "ff02::c"  # TODO: Support other ipv6 multicasts
            self._address = (self.broadcast_ip, port, 0, 0)
        self.sock = socket.socket(af_type, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
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

    def m_search(self):
        data = (
            (
                "M-SEARCH * HTTP/1.1\r\n"
                "HOST: {}:{}\r\n"
                "MAN: ssdp:discover\r\n"
                "MX: 1\r\n"
                "ST: ssdp:all\r\n"
            )
            .format(self.broadcast_ip, self.port)
            .encode("utf-8")
        )
        self.send(data)
        return [x for x in self.recv()]


def discover():
    ms = MulticastSocket()
    responses = ms.m_search()
    ret = []
    for response in responses:
        headers = parse_headers(response)
        ret.append(headers)
    return ret
