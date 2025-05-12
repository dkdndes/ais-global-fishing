#!/usr/bin/env python3
"""
example_trips.py

Display the port-to-port trips detected for a vessel.
"""

from pprint import pprint

from gfw_client_lib import GFWClient


def main():
    client = GFWClient()

    vessel_id = (
        client.search_vessels(
            query="368045130",
            datasets=["public-global-vessel-identity:latest"],
            limit=1,
        )["entries"][0]["selfReportedInfo"][0]["id"]
    )

    trips = client.get_trips(vessel_id)
    print(f"Trips returned: {len(trips)}")
    if trips:
        pprint(trips[0])


if __name__ == "__main__":
    main()
