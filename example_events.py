#!/usr/bin/env python3
"""
example_events.py

Fetch FISHING and PORT_VISIT events of a vessel for the previous month.
"""

from datetime import datetime, timedelta
from pprint import pprint

from gfw_client_lib import GFWClient


def main():
    client = GFWClient()

    # Resolve MMSI (MISS FREYA) → vesselId
    vessel_id = (
        client.search_vessels(
            query="368045130",
            datasets=["public-global-vessel-identity:latest"],
            limit=1,
        )["entries"][0]["selfReportedInfo"][0]["id"]
    )

    end = datetime.utcnow()
    start = end - timedelta(days=30)

    events = client.get_events(
        vessel_id,
        start=start,
        end=end,
        event_types=["FISHING", "PORT_VISIT"],
    )

    print(f"Found {len(events)} events")
    pprint(events[:3])


if __name__ == "__main__":
    main()
