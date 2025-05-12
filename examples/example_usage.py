#!/usr/bin/env python3
"""
example_usage.py

A comprehensive example showing how to use the AIS Global Fishing library
for common vessel search and information retrieval tasks.
"""

from ais_global_fishing import GFWClient
import pprint
from datetime import datetime, timedelta


def main():
    # Initialize the client (API key is read from .env or GLOBALFISHING_WATCH_API_KEY)
    client = GFWClient()
    print("AIS Global Fishing Client initialized successfully")

    # 1) Search for a vessel by MMSI
    print("\n1. Searching for vessel by MMSI...")
    result = client.search_vessels(
        query="368045130",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA"],
        limit=5,
    )

    print(f"Found {len(result.get('entries', []))} vessels")

    # Grab the vessel_id from the first search entry
    if not result.get('entries'):
        print("No vessels found. Exiting.")
        return
        
    entry = result["entries"][0]
    vessel_id = entry["selfReportedInfo"][0]["id"]
    vessel_name = entry.get("name", "Unknown")
    print(f"Selected vessel: {vessel_name} (ID: {vessel_id})")

    # 2) Get detailed vessel information
    print("\n2. Getting detailed vessel information...")
    details = client.get_vessel_details(vessel_id=vessel_id)

    print("\nVessel Details:")
    print(f"Name: {details.get('name', 'Unknown')}")
    print(f"Flag: {details.get('flagState', 'Unknown')}")
    print(f"MMSI: {details.get('mmsi', 'Unknown')}")
    print(f"IMO: {details.get('imo', 'Unknown')}")
    print(f"Vessel Type: {details.get('vesselType', 'Unknown')}")
    
    # 3) Get recent vessel tracks (last 7 days)
    print("\n3. Getting recent vessel tracks (last 7 days)...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    try:
        tracks = client.get_track(
            vessel_id=vessel_id,
            start=start_date,
            end=end_date,
            resolution="1h"
        )
        
        track_points = tracks.get("features", [])
        print(f"Retrieved {len(track_points)} track points")
        
        if track_points:
            # Show the most recent position
            latest_point = track_points[-1]
            if "geometry" in latest_point and "coordinates" in latest_point["geometry"]:
                lon, lat = latest_point["geometry"]["coordinates"]
                timestamp = latest_point["properties"].get("timestamp", "Unknown")
                print(f"Latest position: Lat {lat}, Lon {lon} at {timestamp}")
    
    except FileNotFoundError:
        print("No track data available for this vessel")
    
    # 4) Get vessel events
    print("\n4. Getting vessel events...")
    try:
        events = client.get_events(
            vessel_id=vessel_id,
            start=start_date,
            end=end_date
        )
        
        event_entries = events.get("entries", [])
        print(f"Retrieved {len(event_entries)} events")
        
        # Count events by type
        event_types = {}
        for event in event_entries:
            event_type = event.get("type", "Unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        print("Event types:")
        for event_type, count in event_types.items():
            print(f"- {event_type}: {count}")
            
    except Exception as e:
        print(f"Error retrieving events: {e}")
    
    print("\nExample completed successfully")


if __name__ == "__main__":
    main()
