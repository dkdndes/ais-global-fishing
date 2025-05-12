#!/usr/bin/env python3
"""
example_usage.py

An example showing how to use the gfw_client_lib.
"""

from gfw_client_lib import GFWClient
import pprint

def main():
    # Initialize the client (API key is read from .env or GLOBALFISHING_WATCH_API_KEY)
    client = GFWClient()

    # 1) Search for a vessel by MMSI
    result = client.search_vessels(
        query="368045130",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA"],
        limit=5
    )
    entry = result["entries"][0]
    vessel_id = entry["selfReportedInfo"][0]["id"]
    print(f"Found vessel ID: {vessel_id}")

    # 2) Get detailed vessel information, including ownership
    details = client.get_vessel_details(
        vessel_id=vessel_id,
        includes=["OWNERSHIP"]
    )
    print("\nVessel Details with Ownership:")
    pprint.pp(details)

if __name__ == "__main__":
    main()
