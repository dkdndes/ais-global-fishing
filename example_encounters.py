#!/usr/bin/env python3
"""
example_encounters.py

Request encounter events (possible transhipments) for a vessel in the
last 90 days.
"""

from datetime import datetime, timedelta
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

    end = datetime.utcnow()
    start = end - timedelta(days=90)

    encounters = client.get_encounters(start=start, end=end, vessel_ids=[vessel_id])
    print(f"Encounter events: {len(encounters)}")
    pprint(encounters[:2])


if __name__ == "__main__":
    main()
