#!/usr/bin/env python3
"""
example_bulk_vessels.py

Demonstrate how to retrieve information for multiple vessels in bulk
and perform comparative analysis.
"""

from datetime import datetime, timedelta
import json
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

from ais_global_fishing import GFWClient


def main():
    client = GFWClient()
    print("AIS Global Fishing - Bulk Vessel Analysis Example")
    print("-----------------------------------------------")

    # Step 1: Search for a group of vessels to analyze
    print("\n1. Searching for longline fishing vessels...")
    search_result = client.search_vessels(
        where="vesselType = 'FISHING' AND geartype = 'LONGLINERS'",
        datasets=["public-global-vessel-identity:latest"],
        limit=10
    )
    
    vessel_entries = search_result.get("entries", [])
    if not vessel_entries:
        print("No vessels found matching the criteria. Exiting.")
        return
    
    print(f"Found {len(vessel_entries)} vessels for analysis")
    
    # Extract vessel IDs and basic information
    vessel_ids = []
    vessel_info = {}
    
    for vessel in vessel_entries:
        vessel_id = vessel.get("id")
        if vessel_id:
            vessel_ids.append(vessel_id)
            vessel_info[vessel_id] = {
                "name": vessel.get("name", "Unknown"),
                "flag": vessel.get("flagState", "Unknown"),
                "length": vessel.get("length", "Unknown"),
                "mmsi": vessel.get("mmsi", "Unknown"),
                "imo": vessel.get("imo", "Unknown")
            }
    
    # Step 2: Get detailed information for all vessels in bulk
    print(f"\n2. Retrieving detailed information for {len(vessel_ids)} vessels in bulk...")
    try:
        bulk_details = client.get_vessels_bulk(
            ids=vessel_ids,
            datasets=["public-global-vessel-identity:latest"],
            includes=["OWNERSHIP", "AUTHORIZATIONS"]
        )
        
        vessels_data = bulk_details.get("entries", [])
        print(f"Retrieved details for {len(vessels_data)} vessels")
        
        # Enhance vessel_info with additional details
        for vessel in vessels_data:
            vessel_id = vessel.get("id")
            if vessel_id in vessel_info:
                # Add authorization count
                vessel_info[vessel_id]["auth_count"] = len(vessel.get("authorizations", []))
                
                # Add owner information if available
                owners = vessel.get("ownership", [])
                if owners:
                    vessel_info[vessel_id]["owner"] = owners[0].get("owner", "Unknown")
                    vessel_info[vessel_id]["owner_country"] = owners[0].get("country", "Unknown")
                else:
                    vessel_info[vessel_id]["owner"] = "Unknown"
                    vessel_info[vessel_id]["owner_country"] = "Unknown"
        
        # Display vessel information in a table
        table_data = []
        headers = ["Name", "Flag", "Length", "Owner", "Owner Country", "Authorizations"]
        
        for vessel_id, info in vessel_info.items():
            row = [
                info.get("name", "Unknown"),
                info.get("flag", "Unknown"),
                info.get("length", "Unknown"),
                info.get("owner", "Unknown"),
                info.get("owner_country", "Unknown"),
                info.get("auth_count", 0)
            ]
            table_data.append(row)
        
        print("\nVessel Information:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    except Exception as e:
        print(f"Error retrieving bulk vessel details: {e}")
        return
    
    # Step 3: Define a time period for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    print(f"\n3. Analyzing vessel activity from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    # Step 4: Get fishing events for all vessels
    print("\n4. Retrieving fishing events for all vessels...")
    
    vessel_fishing_data = {}
    for vessel_id in vessel_ids:
        vessel_name = vessel_info[vessel_id]["name"]
        print(f"  Processing {vessel_name}...")
        
        try:
            # Get fishing events for this vessel
            events = client.get_events(
                vessel_id=vessel_id,
                start=start_date,
                end=end_date,
                event_types=["FISHING"]
            )
            
            fishing_events = events.get("entries", [])
            
            # Calculate total fishing hours
            total_hours = 0
            for event in fishing_events:
                duration_seconds = event.get("duration", 0)
                total_hours += duration_seconds / 3600
            
            vessel_fishing_data[vessel_id] = {
                "name": vessel_name,
                "event_count": len(fishing_events),
                "fishing_hours": round(total_hours, 1)
            }
            
            print(f"    Found {len(fishing_events)} fishing events ({round(total_hours, 1)} hours)")
            
        except Exception as e:
            print(f"    Error retrieving fishing events: {e}")
            vessel_fishing_data[vessel_id] = {
                "name": vessel_name,
                "event_count": 0,
                "fishing_hours": 0
            }
    
    # Step 5: Visualize the results
    print("\n5. Creating visualization of fishing activity...")
    
    try:
        # Extract data for plotting
        vessel_names = [data["name"] for _, data in vessel_fishing_data.items()]
        fishing_hours = [data["fishing_hours"] for _, data in vessel_fishing_data.items()]
        
        # Create a bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(vessel_names, fishing_hours, color='skyblue')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}h',
                    ha='center', va='bottom', rotation=0)
        
        plt.title('Fishing Hours by Vessel (Last 60 Days)')
        plt.xlabel('Vessel Name')
        plt.ylabel('Fishing Hours')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the figure
        plt.savefig('fishing_hours_comparison.png')
        print("Chart saved as fishing_hours_comparison.png")
        
        # Save the data to a JSON file for further analysis
        with open("vessel_fishing_data.json", "w") as f:
            json.dump(vessel_fishing_data, f, indent=2)
        print("Data saved to vessel_fishing_data.json")
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        print("Note: To create visualizations, install matplotlib: pip install matplotlib")
    
    print("\nBulk vessel analysis complete!")


if __name__ == "__main__":
    main()
