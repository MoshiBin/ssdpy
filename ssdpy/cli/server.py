# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
from ..version import VERSION
from ..server import SSDPServer

logging.basicConfig()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Start an SSDP server")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s {}".format(VERSION))
    parser.add_argument("-v", "--verbose", help="Be more verbose", action="store_true")
    proto_group = parser.add_mutually_exclusive_group()
    proto_group.add_argument("-4", "--ipv4", help="Listen on IPv4 (default: True)", action="store_true")
    proto_group.add_argument("-6", "--ipv6", help="Listen on IPv6 instead of IPv4", action="store_true")
    parser.add_argument("usn", help="Unique server name", nargs=1)
    parser.add_argument(
        "-t",
        "--device-type",
        help="Device type. Affects the NT field (default: ssdp:rootdevice)",
        default="ssdp:rootdevice",
    )
    parser.add_argument("-i", "--iface", help="Listen on a specific network interface")
    parser.add_argument(
        "-p",
        "--port",
        help="Listen on this port (default: 1900)",
        default=1900,
        type=int,
    )
    parser.add_argument(
        "--max-age",
        help="The amount of seconds that the server info should be cached for (default: do not cache)",
        type=int,
    )
    parser.add_argument(
        "-l",
        "--location",
        help="Location that notifications should point to. This sets both LOCATION and AL",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="Address of the interface to listen on. Only valid for IPv4.",
    )
    parser.add_argument(
        "-e",
        "--extra-field",
        action="append",
        nargs=2,
        metavar=("NAME", "VALUE"),
        help="Extra fields to pass in NOTIFY packets. Pass multiple times for multiple extra headers",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    extra_fields = None
    if args.extra_field is not None:
        extra_fields = dict(args.extra_field)

    if args.ipv6:
        proto = "ipv6"
    else:
        proto = "ipv4"

    if args.iface is not None:
        args.iface = args.iface.encode("utf-8")

    server = SSDPServer(
        args.usn[0],
        proto=proto,
        device_type=args.device_type,
        port=args.port,
        iface=args.iface,
        address=args.address,
        max_age=args.max_age,
        al=args.location,
        location=args.location,
        extra_fields=extra_fields,
    )

    logger = logging.getLogger("ssdpy.server")
    logger.setLevel(logging.INFO)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.error("Keyboard interrupt received, shutting down")
