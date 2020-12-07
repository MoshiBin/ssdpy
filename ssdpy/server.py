# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import socket
import struct
from .constants import ipv6_multicast_ip, ipv4_multicast_ip
from .protocol import create_notify_payload
from .http_helper import parse_headers
from .compat import if_nametoindex, SO_BINDTODEVICE


logger = logging.getLogger("ssdpy.server")


class SSDPServer(object):
    """
    A server that can listen to SSDP M-SEARCH requests and responds with appropriate NOTIFY packets when the ST matches its device_type.

    Example usage::

    >>> server = SSDPServer("my-service", device_type="my-device-type")
    >>> server.serve_forever()

    This will listen to SSDP M-Searches (discovery) and respond with

    :param usn: A unique service name, which identifies your service.
    :type usn: str
    :param proto: Protocol to use, either ``ipv4`` or ``ipv6``. Defaults to ``ipv4.``
    :type proto: str, optional
    :param device_type: The device type to respond as. Defaults to ``ssdp:rootdevice`` which is the base type for ssdp devices.
    :type device_type: str, optional
    :param port: Port to listen on. SSDP works on port 1900, which is the default value here.
    :type port: int, optional
    :param iface: Interface to bind to. When not provided, the operating system decides which interface should handle multicasts and binds to it.
    :type iface: bytes, optional
    :param address: A specific address to bind to. This is required when using IPv6, since you will have a link-local IP address in addition to at least one actual IP address.
    :type address: str, optional
    :param max_age: The maximum time, in seconds, for clients to cache notifications.
    :type max_age: int
    :param location: Canonical URL of the service.
    :type location: str
    :param al: Canonical URL of the service, but only supported in the IETF version of SSDP. Should be the same as ``location``.
    :type al: str
    :param extra_fields: Extra header fields to send. UPnP SSDP section 1.1.3 allows for extra vendor-specific fields to be sent in the NOTIFY packet. According to the spec, the field names MUST be in the format of `token`.`domain-name`, for example `myheader.philips.com`. SSDPy, however, does not check this and allows any field name - as long as it's ASCII.
    :type extra_fields: dict
    """

    def __init__(
        self,
        usn,
        proto="ipv4",
        device_type="ssdp:rootdevice",
        port=1900,
        iface=None,
        address=None,
        max_age=None,
        location=None,
        al=None,
        extra_fields=None,
    ):
        allowed_protos = ("ipv4", "ipv6")
        if proto not in allowed_protos:
            raise ValueError("Invalid proto - expected one of {}".format(allowed_protos))
        self.stopped = False
        self.usn = usn
        self.device_type = device_type
        self.al = al
        self.location = location
        self.max_age = max_age
        self._iface = iface

        self._extra_fields = {}
        if extra_fields is not None:
            for field, value in extra_fields.items():
                try:
                    field.encode("ascii")
                    value.encode("ascii")
                    self._extra_fields[field] = value
                except (UnicodeDecodeError, UnicodeEncodeError):
                    raise ValueError("Invalid value for extra_field: %s=%s is not ASCII", field, value)

        if proto == "ipv4":
            self._af_type = socket.AF_INET
            self._broadcast_ip = ipv4_multicast_ip
            self._address = (self._broadcast_ip, port)
            bind_address = "0.0.0.0"
        elif proto == "ipv6":
            self._af_type = socket.AF_INET6
            self._broadcast_ip = ipv6_multicast_ip
            self._address = (self._broadcast_ip, port, 0, 0)
            bind_address = "::"

        self.sock = socket.socket(self._af_type, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to specific interface
        if iface is not None:
            self.sock.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, iface)

        # Subscribe to multicast address
        if proto == "ipv4":
            mreq = socket.inet_aton(self._broadcast_ip)
            if address is not None:
                mreq += socket.inet_aton(address)
            else:
                mreq += struct.pack(b"@I", socket.INADDR_ANY)
            self.sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq,
            )
            # Allow multicasts on loopback devices (necessary for testing)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        elif proto == "ipv6":
            # In IPv6 we use the interface index, not the address when subscribing to the group
            mreq = socket.inet_pton(socket.AF_INET6, self._broadcast_ip)
            if iface is not None:
                iface_index = if_nametoindex(iface)
                # Send outgoing packets from the same interface
                self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, iface_index)
                mreq += struct.pack(b"@I", iface_index)
            else:
                mreq += socket.inet_pton(socket.AF_INET6, "::")
            self.sock.setsockopt(
                socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq,
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
        if data.startswith(b"M-SEARCH") and (headers.get("st") == self.device_type or headers.get("st") == "ssdp:all"):
            logger.info("Received qualifying M-SEARCH from {}".format(address))
            logger.debug("M-SEARCH data: {}".format(headers))
            notify = create_notify_payload(
                host=self._broadcast_ip,
                nt=self.device_type,
                usn=self.usn,
                location=self.location,
                al=self.al,
                max_age=self.max_age,
                extra_fields=self._extra_fields,
            )
            logger.debug("Created NOTIFY: {}".format(notify))
            try:
                self.sock.sendto(notify, address)
            except OSError as e:
                # Most commonly: We received a multicast from an IP not in our subnet
                logger.debug("Unable to send NOTIFY to {}: {}".format(address, e))

    def serve_forever(self):
        """
        Start listening for M-SEARCH discovery attempts and answer any that refers to our ``device_type`` or to ``ssdp:all``. This will block execution until an exception occurs.
        """
        logger.info("Listening forever")
        try:
            while not self.stopped:
                data, address = self.sock.recvfrom(1024)
                self.on_recv(data, address)
        except Exception:
            self.sock.close()
            raise
