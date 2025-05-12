#!/usr/bin/env python3
"""
example_bulk_vessels.py

Demonstrate the bulk ``/vessels`` endpoint with additional parameters
such as registries-info-data and binary flag.
"""

from pprint import pprint

from gfw_client_lib import GFWClient


def main():
    client = GFWClient()

    ids = [
        "90ab31dfb-bcab-a05f-d12f-2544e1869205",
        "145876a6e-e741-d4e7-67c9-0e7be0ff33b7",
    ]

    vessels = client.get_vessels_bulk(
        ids=ids,
        datasets=["public-global-vessel-identity:latest"],
        includes=["POTENTIAL_RELATED_SELF_REPORTED_INFO"],
        registries_info_data="ALL",
        binary=False,
    )

    print(f"Returned {len(vessels)} vessel records")
    pprint(vessels[0])


if __name__ == "__main__":
    main()
