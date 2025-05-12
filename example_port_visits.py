#!/usr/bin/env python3
"""
example_port_visits.py

List every port visit of a vessel over the last 365 days.
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
    start = end - timedelta(days=365)

    visits = client.get_port_visits(start=start, end=end, vessel_ids=[vessel_id])
    print(f"Total visits: {len(visits)}")
    if visits:
        pprint(visits[0])


if __name__ == "__main__":
    main()
