# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import socket
from .constants import IPv4, IPv6, ipv6_multicast_ip, ipv4_multicast_ip
from .protocol import create_notify_payload
from .http_helper import parse_headers


logger = logging.getLogger("ssdpy.server")


class SSDPServer(object):
    def __init__(
        self,
        usn,
        proto=IPv4,
        device_type="ssdp:rootdevice",
        port=1900,
        iface=None,
        max_age=None,
        location=None,
        al=None,
    ):
        """
        A server that listens to SSDP M-SEARCH requests and responds with appropriate NOTIFY
        packets when the ST matches its device_type.

        Usage:
        >>> server = SSDPServer("my-service", device_type="my-device-type")
        >>> server.serve_forever()
        """
        allowed_protos = (IPv4, IPv6)
        if proto not in allowed_protos:
            raise ValueError(
                "Invalid proto - expected one of {}".format(allowed_protos)
            )
        self.stopped = False
        self.usn = usn
        self.device_type = device_type
        self.al = al
        self.location = location
        self.max_age = max_age
        self._iface = iface
        if proto is IPv4:
            self._af_type = socket.AF_INET
            self._broadcast_ip = ipv4_multicast_ip
            self._address = (self._broadcast_ip, port)
            bind_address = "0.0.0.0"
        elif proto is IPv6:
            self._af_type = socket.AF_INET6
            self._broadcast_ip = ipv6_multicast_ip
            self._address = (self._broadcast_ip, port, 0, 0)
            bind_address = "::"
        self.sock = socket.socket(self._af_type, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if iface is not None:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, iface)
        if proto is IPv4:
            self.sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(self._broadcast_ip) + socket.inet_aton("0.0.0.0"),
            )
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        elif proto is IPv6:
            self.sock.setsockopt(
                socket.IPPROTO_IPV6,
                socket.IPV6_JOIN_GROUP,
                socket.inet_pton(socket.AF_INET6, self._broadcast_ip)
                + socket.inet_pton(socket.AF_INET6, "::"),
            )
            self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        self.sock.bind((bind_address, port))

    def on_recv(self, data, address):
        logger.debug("Received packet from {}: {}".format(address, data))
        try:
            headers = parse_headers(data)
        except ValueError:
            # Not an SSDP M-SEARCH; ignore.
            logger.debug("NOT M-SEARCH - SKIPPING")
            pass
        if data.startswith(b"M-SEARCH") and (
            headers.get("st") == self.device_type or headers.get("st") == "ssdp:all"
        ):
            logger.info("Received qualifying M-SEARCH from {}".format(address))
            logger.debug("M-SEARCH data: {}".format(headers))
            notify = create_notify_payload(
                self._broadcast_ip,
                self.device_type,
                self.usn,
                self.location,
                self.al,
                self.max_age,
            )
            logger.debug("Created NOTIFY: {}".format(notify))
            self.sock.sendto(notify, address)

    def serve_forever(self):
        logger.info("Listening forever")
        try:
            while not self.stopped:
                data, address = self.sock.recvfrom(1024)
                self.on_recv(data, address)
        except Exception:
            self.sock.close()
            raise
