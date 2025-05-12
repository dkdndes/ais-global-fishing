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
        limit=5,
    )

    # Grab the vessel_id from the first search entry
    entry = result["entries"][0]
    vessel_id = entry["selfReportedInfo"][0]["id"]
    print(f"Found vessel ID: {vessel_id}")

    # 2) Get detailed vessel information
    # NOTE:  Requesting the 'OWNERSHIP' include caused a 422 error.  The plain
    #        detail request (mirroring vessel_finder.py) succeeds, so we omit
    #        the includes parameter here.
    details = client.get_vessel_details(vessel_id=vessel_id)

    print("\nVessel Details:")
    pprint.pp(details)


if __name__ == "__main__":
    main()
