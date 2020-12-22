# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import socket
import ctypes
import errno
import sys


PY2 = sys.version_info[0] == 2
WINDOWS = sys.platform == "win32"
LINUX = sys.platform == "linux"

string_types = basestring if PY2 else str  # noqa


# Python 2 doesn't have socket.if_nametoindex so we need to implement it manually
if LINUX:
    if PY2:
        import ctypes.util

        libc = ctypes.CDLL(ctypes.util.find_library("c"))

        def if_nametoindex(name):
            """
            Return the logical index number of the given interface name.
            This is backported for Python 2.7 on Linux.
            """
            if not isinstance(name, string_types):
                raise TypeError("Expected string type, got '{}'".format(type(name)))

            rc = libc.if_nametoindex(name)
            if rc == 0:
                raise OSError("no interface with this name '{}'".format(name))
            return rc

    else:
        if_nametoindex = socket.if_nametoindex
else:

    def if_nametoindex(name):
        raise NotImplementedError("if_nametoindex is not available on this platform")


SO_BINDTODEVICE = getattr(socket, "SO_BINDTODEVICE", 25)


if PY2 and WINDOWS:
    IPPROTO_IPV6 = 41

    def inet_pton(socket_af, ip_address):
        """
        Python 2.7 on Windows doesn't have the inet_pton function, which SSDPy uses for IPv6
        servers. This function backports inet_pton using raw winsock functions.
        This should ONLY be used on Python 2.7 on Windows.
        """
        if socket_af != socket.AF_INET6 or sys.platform != "win32":
            raise ValueError("inet_pton workaround function only works for IPv6 on Windows")

        # typedef struct in6_addr {
        #     union {
        #         u_char  Byte[16];
        #         u_short Word[8];
        #     } u;
        # } IN6_ADDR, *PIN6_ADDR, FAR *LPIN6_ADDR;
        in6_addr = ctypes.c_ubyte * 16

        # INT WSAAPI InetPtonW(
        #     INT    Family,
        #     PCWSTR pszAddrString,
        #     PVOID  pAddrBuf
        # );
        InetPtonW = ctypes.windll.ws2_32.InetPtonW
        WSAGetLastError = ctypes.windll.ws2_32.WSAGetLastError

        socket_af = ctypes.c_int(socket.AF_INET6)
        ip_address = ctypes.c_wchar_p(ip_address)
        address_buffer = in6_addr()
        return_code = InetPtonW(socket_af, ip_address, address_buffer)
        if return_code != 1:
            error_code = WSAGetLastError()
            raise OSError("inet_pton failed: %s", errno.errorcode.get(error_code))
        else:
            return ctypes.string_at(address_buffer, 16)


else:
    IPPROTO_IPV6 = socket.IPPROTO_IPV6
    inet_pton = socket.inet_pton
