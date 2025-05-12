#!/usr/bin/env python3
"""
example_events.py

Demonstrate how to retrieve and analyze vessel behavioral events
such as fishing activity, port visits, and encounters.
"""

from datetime import datetime, timedelta
import json
from pprint import pprint
from collections import Counter

from ais_global_fishing import GFWClient


def main():
    client = GFWClient()
    print("AIS Global Fishing - Vessel Events Example")
    print("-----------------------------------------")

    # Define time period (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    print(f"Analyzing events from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    # Step 1: Find a vessel to analyze
    print("\n1. Searching for fishing vessels...")
    search_result = client.search_vessels(
        where="vesselType = 'FISHING'",
        datasets=["public-global-vessel-identity:latest"],
        limit=5
    )
    
    if not search_result.get("entries"):
        print("No fishing vessels found. Exiting.")
        return
    
    # Select the first vessel from the results
    vessel = search_result["entries"][0]
    vessel_id = vessel.get("id")
    vessel_name = vessel.get("name", "Unknown")
    vessel_flag = vessel.get("flagState", "Unknown")
    
    print(f"Selected vessel: {vessel_name} (Flag: {vessel_flag}, ID: {vessel_id})")
    
    # Step 2: Get all events for this vessel
    print("\n2. Retrieving all events for the selected vessel...")
    try:
        events = client.get_events(
            vessel_id=vessel_id,
            start=start_date,
            end=end_date
        )
        
        event_entries = events.get("entries", [])
        print(f"Retrieved {len(event_entries)} events")
        
        if event_entries:
            # Count events by type
            event_types = Counter([event.get("type", "Unknown") for event in event_entries])
            
            print("\nEvent types distribution:")
            for event_type, count in event_types.items():
                print(f"- {event_type}: {count} events")
            
            # Show example of each event type
            print("\nExample of each event type:")
            shown_types = set()
            for event in event_entries:
                event_type = event.get("type", "Unknown")
                if event_type not in shown_types:
                    print(f"\n{event_type} event example:")
                    pprint(event)
                    shown_types.add(event_type)
        else:
            print("No events found for this vessel in the specified time period.")
    
    except Exception as e:
        print(f"Error retrieving events: {e}")
    
    # Step 3: Get specific event types
    print("\n3. Retrieving fishing events for all vessels...")
    try:
        fishing_events = client.get_fishing_events(
            start=start_date,
            end=end_date,
            vessel_ids=None  # Get for all vessels
        )
        
        fishing_entries = fishing_events.get("entries", [])
        print(f"Retrieved {len(fishing_entries)} fishing events")
        
        if fishing_entries:
            # Count fishing events by vessel
            vessel_counts = Counter()
            for event in fishing_entries:
                vessel_counts[event.get("vesselId", "Unknown")] += 1
            
            print("\nTop 5 vessels with most fishing events:")
            for vessel_id, count in vessel_counts.most_common(5):
                print(f"- Vessel ID {vessel_id}: {count} fishing events")
            
            # Save fishing events to a JSON file for further analysis
            with open("fishing_events.json", "w") as f:
                json.dump(fishing_entries[:10], f, indent=2)  # Save first 10 events as example
            print("\nSample fishing events saved to fishing_events.json")
        else:
            print("No fishing events found in the specified time period.")
    
    except Exception as e:
        print(f"Error retrieving fishing events: {e}")
    
    # Step 4: Get vessel encounters (possible transshipments)
    print("\n4. Retrieving vessel encounters...")
    try:
        encounters = client.get_encounters(
            start=start_date,
            end=end_date
        )
        
        encounter_entries = encounters.get("entries", [])
        print(f"Retrieved {len(encounter_entries)} vessel encounters")
        
        if encounter_entries and len(encounter_entries) > 0:
            # Show an example encounter
            print("\nExample encounter:")
            example = encounter_entries[0]
            encounter_info = {
                "Encounter ID": example.get("id", "Unknown"),
                "Start Time": example.get("startTime", "Unknown"),
                "End Time": example.get("endTime", "Unknown"),
                "Duration (hours)": round(example.get("duration", 0) / 3600, 2),
                "Vessel 1": example.get("vessel1Id", "Unknown"),
                "Vessel 2": example.get("vessel2Id", "Unknown"),
                "Mean Latitude": example.get("meanLatitude", "Unknown"),
                "Mean Longitude": example.get("meanLongitude", "Unknown")
            }
            
            for key, value in encounter_info.items():
                print(f"{key}: {value}")
        else:
            print("No encounters found in the specified time period.")
    
    except Exception as e:
        print(f"Error retrieving encounters: {e}")


if __name__ == "__main__":
    main()
