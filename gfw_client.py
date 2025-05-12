#!/usr/bin/env python3
"""
gfw_client.py

Small convenience CLI around **gfw_client_lib.GFWClient**.

It replaces the old proof-of-concept that depended on the (unrelated)
`gfwapiclient` package.  The new version relies exclusively on the local
`gfw_client_lib` already present in this repository.

Usage
-----

Search a vessel (MMSI / IMO / name) and print the first match:

    python gfw_client.py search 368045130

Get the full identity record of a known vessel-id:

    python gfw_client.py details 3312b30d6-65b6-1bdb-6a78-3f5eb3977e58
"""

from __future__ import annotations

import argparse
import sys
from pprint import pprint

from gfw_client_lib import GFWClient


def cmd_search(args: argparse.Namespace) -> None:
    """Handle the `search` sub-command."""
    client = GFWClient()
    result = client.search_vessels(
        query=args.query,
        where=args.where,
        limit=args.limit,
        datasets=["public-global-vessel-identity:latest"],
        includes=args.include,
        binary=not args.no_binary,
    )

    entries = result.get("entries", [])
    if not entries:
        print("No vessels found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(entries)} entries – showing the first one:\n")
    pprint(entries[0])


def cmd_details(args: argparse.Namespace) -> None:
    """Handle the `details` sub-command."""
    client = GFWClient()
    details = client.get_vessel_details(
        vessel_id=args.vessel_id,
        includes=args.include,
    )
    pprint(details)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI helper for the Global Fishing Watch Gateway v3 API"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search -------------------------------------------------------------
    p_search = sub.add_parser("search", help="Search vessels by query or where clause")
    p_search.add_argument("query", nargs="?", help="Text query (MMSI, IMO, name …)")
    p_search.add_argument("--where", help="SQL-like where clause")
    p_search.add_argument(
        "-i",
        "--include",
        action="append",
        metavar="SECTION",
        help="Include section (e.g. OWNERSHIP)",
    )
    p_search.add_argument("-l", "--limit", type=int, default=10, help="Max results")
    p_search.add_argument("--no-binary", action="store_true", help="Disable binary flag")
    p_search.set_defaults(func=cmd_search)

    # details ------------------------------------------------------------
    p_details = sub.add_parser("details", help="Get full identity of a vessel")
    p_details.add_argument("vessel_id", help="GFW vessel-id")
    p_details.add_argument(
        "-i",
        "--include",
        action="append",
        metavar="SECTION",
        help="Include section (comma-joined for /vessels/{id})",
    )
    p_details.set_defaults(func=cmd_details)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
