# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
import pprint
from ..version import VERSION
from ..client import SSDPClient
from ..constants import IPv4, IPv6

logging.basicConfig()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run an SSDP M-SEARCH",)
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(VERSION)
    )
    parser.add_argument("-v", "--verbose", help="Be more verbose", action="store_true")
    proto_group = parser.add_mutually_exclusive_group()
    proto_group.add_argument(
        "-4", "--ipv4", help="Listen on IPv4 (default: True)", action="store_true"
    )
    proto_group.add_argument(
        "-6", "--ipv6", help="Listen on IPv6 instead of IPv4", action="store_true"
    )
    parser.add_argument(
        "-t", "--ttl", help="TTL for the M-SEARCH (default: 2)", default=2
    )
    parser.add_argument(
        "-o",
        "--timeout",
        help="Maximum timeout for connections (default: 5)",
        default=5,
    )
    parser.add_argument("ST", help="Type of device to search for (ST)", nargs=1)
    parser.add_argument("-i", "--iface", help="Listen on a specific network interface")
    parser.add_argument(
        "-p", "--port", help="Send on this port (default: 1900)", default=1900
    )
    parser.add_argument(
        "-m", "--mx", help="Maximum wait time for response (default 1s)", default=1
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.ipv6:
        proto = IPv6
    else:
        proto = IPv4

    if args.iface is not None:
        args.iface = args.iface.encode("utf-8")

    client = SSDPClient(
        proto=proto,
        port=args.port,
        ttl=args.ttl,
        iface=args.iface,
        timeout=args.timeout,
    )

    logger = logging.getLogger("ssdpy.client")
    logger.setLevel(logging.INFO)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    response = client.m_search(st=args.ST[0], mx=args.mx)
    for device in response:
        pprint.pprint(device)
