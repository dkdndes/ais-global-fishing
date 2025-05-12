#!/usr/bin/env python3
"""
example_search_advanced.py

Demonstrate advanced search capabilities:
  • binary flag
  • `where` queries with gear-type, flag, etc.
  • extra includes
"""

from pprint import pprint

from gfw_client_lib import GFWClient


def main():
    client = GFWClient()

    # Example 1 ─ vessels flagged CHN (non-binary response)
    res_flag = client.search_vessels(
        where="flag = 'CHN'",
        datasets=["public-global-vessel-identity:latest"],
        binary=False,
        limit=3,
    )
    print("CHN flagged vessels (first 3):")
    pprint([e["registryInfo"][0]["shipname"] for e in res_flag["entries"]])

    # Example 2 ─ purse-seine vessels
    res_gear = client.search_vessels(
        where="geartypes='TUNA_PURSE_SEINES'",
        datasets=["public-global-vessel-identity:latest"],
        binary=False,
        limit=3,
    )
    print("\nTuna purse-seiners (first 3):")
    pprint([e["registryInfo"][0]["shipname"] for e in res_gear["entries"]])

    # Example 3 ─ query by IMO with extra includes
    res_imo = client.search_vessels(
        query="9111694",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA", "OWNERSHIP"],
        limit=1,
    )
    print("\nResult with OWNERSHIP include:")
    pprint(res_imo["entries"][0])


if __name__ == "__main__":
    main()
