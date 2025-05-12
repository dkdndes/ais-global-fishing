#!/usr/bin/env python3
"""
example_track.py

Retrieve the AIS track for the last 7 days of a vessel located via MMSI
and print the number of track points returned.
"""

from datetime import datetime, timedelta
from pprint import pprint

from gfw_client_lib import GFWClient


def main():
    client = GFWClient()

    # Resolve MMSI → vesselId
    search = client.search_vessels(
        query="368045130",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA"],
        limit=1,
    )
    vessel_id = search["entries"][0]["selfReportedInfo"][0]["id"]
    print("vesselId:", vessel_id)

    # Last seven days
    now = datetime.utcnow()
    start = now - timedelta(days=7)

    track = client.get_track(vessel_id, start=start, end=now, resolution="1h")
    print(f"Received {len(track)} track points")
    pprint(track[:5])  # show first 5 points


if __name__ == "__main__":
    main()
