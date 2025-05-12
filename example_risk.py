#!/usr/bin/env python3
"""
example_risk.py

Show the risk/compliance scores of a vessel (requires account permissions).
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

    try:
        risk = client.get_risk(vessel_id)
    except Exception as exc:  # noqa: BLE001
        print("Risk endpoint not permitted or not available:", exc)
    else:
        pprint(risk)


if __name__ == "__main__":
    main()
