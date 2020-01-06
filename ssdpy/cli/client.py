# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import json
import logging
import pprint
from ..version import VERSION
from ..client import SSDPClient

logging.basicConfig()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run an SSDP M-SEARCH",)
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(VERSION)
    )
    parser.add_argument("-v", "--verbose", help="Be more verbose", action="store_true")
    parser.add_argument(
        "-6", "--ipv6", help="Listen on IPv6 instead of IPv4", action="store_true"
    )
    parser.add_argument(
        "-t", "--ttl", help="TTL for the M-SEARCH (default: 2)", default=2, type=int
    )
    parser.add_argument(
        "-o",
        "--timeout",
        help="Maximum timeout for connections (default: 5)",
        default=5,
        type=int,
    )
    parser.add_argument("ST", help="Type of device to search for (ST)", nargs=1)
    parser.add_argument("-i", "--iface", help="Listen on a specific network interface")
    parser.add_argument("-a", "--address", help="Bind to this address")
    parser.add_argument(
        "-p", "--port", help="Send on this port (default: 1900)", default=1900, type=int
    )
    parser.add_argument(
        "-m",
        "--mx",
        help="Maximum wait time for response (default 1s)",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-j", "--json", help="Format output as JSON", action="store_true",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.ipv6:
        proto = "ipv6"
    else:
        proto = "ipv4"

    if args.iface is not None:
        args.iface = args.iface.encode("utf-8")

    client = SSDPClient(
        proto=proto,
        port=args.port,
        ttl=args.ttl,
        iface=args.iface,
        timeout=args.timeout,
        address=args.address,
    )

    logger = logging.getLogger("ssdpy.client")
    logger.setLevel(logging.INFO)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    response = client.m_search(st=args.ST[0], mx=args.mx)
    if args.json:
        print(json.dumps(response))
    else:
        for device in response:
            pprint.pprint(device)
