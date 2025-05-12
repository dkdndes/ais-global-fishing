#!/usr/bin/env python3
"""
example_port_visits.py

Demonstrate how to retrieve and analyze port visits for vessels.

Run with:
    uv run python examples/example_port_visits.py
"""

from datetime import datetime, timedelta
import json
from collections import Counter
from tabulate import tabulate

from ais_global_fishing import GFWClient


def main():
    client = GFWClient()
    print("AIS Global Fishing - Port Visits Example")
    print("---------------------------------------")

    # Define time period (last 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    print(f"Analyzing port visits from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    # Step 1: Find a vessel to analyze
    print("\n1. Searching for cargo vessels...")
    search_result = client.search_vessels(
        where="vesselType = 'CARGO'",
        datasets=["public-global-vessel-identity:latest"],
        limit=5
    )
    
    if not search_result.get("entries"):
        print("No cargo vessels found. Exiting.")
        return
    
    # Select the first vessel from the results
    vessel = search_result["entries"][0]
    vessel_id = vessel.get("id")
    vessel_name = vessel.get("name", "Unknown")
    vessel_flag = vessel.get("flagState", "Unknown")
    
    print(f"Selected vessel: {vessel_name} (Flag: {vessel_flag}, ID: {vessel_id})")
    
    # Step 2: Get port visits for this vessel
    print(f"\n2. Retrieving port visits for {vessel_name}...")
    try:
        vessel_visits = client.get_port_visits(
            start=start_date,
            end=end_date,
            vessel_ids=[vessel_id]
        )
        
        visit_entries = vessel_visits.get("entries", [])
        print(f"Retrieved {len(visit_entries)} port visits")
        
        if visit_entries:
            # Create a table of port visits
            table_data = []
            headers = ["Port Name", "Country", "Start Date", "End Date", "Duration (hours)"]
            
            for visit in visit_entries:
                port_name = visit.get("portName", "Unknown")
                country = visit.get("country", "Unknown")
                start_time = visit.get("startTime", "Unknown")
                end_time = visit.get("endTime", "Unknown")
                
                # Calculate duration in hours if timestamps are available
                duration = "Unknown"
                if isinstance(start_time, str) and isinstance(end_time, str):
                    try:
                        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                        duration_hours = round((end_dt - start_dt).total_seconds() / 3600, 1)
                        duration = f"{duration_hours} hours"
                    except:
                        pass
                
                table_data.append([port_name, country, start_time, end_time, duration])
            
            print("\nPort visits for this vessel:")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Count visits by port
            port_counts = Counter([visit.get("portName", "Unknown") for visit in visit_entries])
            
            print("\nMost visited ports:")
            for port, count in port_counts.most_common():
                print(f"- {port}: {count} visits")
        else:
            print("No port visits found for this vessel in the specified time period.")
    
    except Exception as e:
        print(f"Error retrieving port visits: {e}")
    
    # Step 3: Get port visits for all vessels to a specific country
    print("\n3. Analyzing port visits to a specific country (e.g., Spain)...")
    try:
        # First get all port visits
        all_visits = client.get_port_visits(
            start=start_date,
            end=end_date
        )
        
        all_visit_entries = all_visits.get("entries", [])
        print(f"Retrieved {len(all_visit_entries)} total port visits")
        
        # Filter for visits to Spain
        country_code = "ESP"  # ISO code for Spain
        country_visits = [v for v in all_visit_entries if v.get("country") == country_code]
        
        print(f"Found {len(country_visits)} visits to ports in {country_code}")
        
        if country_visits:
            # Count visits by port within the country
            port_counts = Counter([visit.get("portName", "Unknown") for visit in country_visits])
            
            print(f"\nMost visited ports in {country_code}:")
            for port, count in port_counts.most_common(5):
                print(f"- {port}: {count} visits")
            
            # Count visits by vessel type
            vessel_types = {}
            for visit in country_visits:
                vessel_id = visit.get("vesselId")
                if vessel_id and vessel_id not in vessel_types:
                    try:
                        # Get vessel details to determine type
                        vessel_details = client.get_vessel_details(vessel_id=vessel_id)
                        vessel_type = vessel_details.get("vesselType", "Unknown")
                        vessel_types[vessel_id] = vessel_type
                    except:
                        vessel_types[vessel_id] = "Unknown"
            
            type_counts = Counter(vessel_types.values())
            
            print(f"\nTypes of vessels visiting {country_code}:")
            for vessel_type, count in type_counts.most_common():
                print(f"- {vessel_type}: {count} vessels")
        else:
            print(f"No visits to {country_code} found in the specified time period.")
    
    except Exception as e:
        print(f"Error analyzing country port visits: {e}")
    
    # Step 4: Get trips for the vessel
    print(f"\n4. Retrieving trips for {vessel_name}...")
    try:
        trips = client.get_trips(vessel_id=vessel_id)
        
        trip_entries = trips.get("entries", [])
        print(f"Retrieved {len(trip_entries)} trips")
        
        if trip_entries:
            # Create a table of trips
            table_data = []
            headers = ["From Port", "To Port", "Departure", "Arrival", "Duration (days)"]
            
            for trip in trip_entries:
                from_port = trip.get("fromPortName", "Unknown")
                to_port = trip.get("toPortName", "Unknown")
                departure = trip.get("departureTime", "Unknown")
                arrival = trip.get("arrivalTime", "Unknown")
                
                # Calculate duration in days if timestamps are available
                duration = "Unknown"
                if isinstance(departure, str) and isinstance(arrival, str):
                    try:
                        departure_dt = datetime.fromisoformat(departure.replace('Z', '+00:00'))
                        arrival_dt = datetime.fromisoformat(arrival.replace('Z', '+00:00'))
                        duration_days = round((arrival_dt - departure_dt).total_seconds() / 86400, 1)
                        duration = f"{duration_days} days"
                    except:
                        pass
                
                table_data.append([from_port, to_port, departure, arrival, duration])
            
            print("\nTrips for this vessel:")
            print(tabulate(table_data[:5], headers=headers, tablefmt="grid"))
            print(f"(Showing 5 of {len(trip_entries)} trips)")
            
            # Save all trips to a JSON file for further analysis
            with open("vessel_trips.json", "w") as f:
                json.dump(trip_entries, f, indent=2)
            print("\nAll trips saved to vessel_trips.json")
        else:
            print("No trips found for this vessel.")
    
    except Exception as e:
        print(f"Error retrieving trips: {e}")


if __name__ == "__main__":
    main()
