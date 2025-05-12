#!/usr/bin/env python3
"""
example_track.py

Retrieve the AIS track for the last 7 days of a vessel located via MMSI
and visualize the track on a map.

Run with:
    uv run python examples/example_track.py
"""

from datetime import datetime, timedelta, timezone
from pprint import pprint
import json
import os

# Try to import folium for map visualization, but continue if not available
try:
    import folium
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False
    print("Note: Install folium package for map visualization: pip install folium")

from ais_global_fishing import GFWClient


def main():
    client = GFWClient()
    print("Initializing AIS Global Fishing client...")

    # Resolve MMSI → vesselId
    print("Searching for vessel with MMSI 368045130...")
    search = client.search_vessels(
        query="368045130",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA"],
        limit=1,
    )
    
    if not search.get("entries"):
        print("No vessels found with this MMSI.")
        return
        
    vessel_id = search["entries"][0]["selfReportedInfo"][0]["id"]
    vessel_name = search["entries"][0].get("name", "Unknown Vessel")
    print(f"Found vessel: {vessel_name}")
    print(f"Vessel ID: {vessel_id}")

    # Last seven days (timezone-aware, UTC)
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=7)
    print(f"Retrieving track from {start.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}...")

    try:
        track_data = client.get_track(vessel_id, start=start, end=now, resolution="1h")
        
        # Extract features from the track data
        features = track_data.get("features", [])
        print(f"Received {len(features)} track points")
        
        if not features:
            print("No track points found in the specified time period.")
            return
            
        # Print the first track point as an example
        print("\nExample track point:")
        if features:
            pprint(features[0])
        
        # Create a map visualization if folium is available
        if HAS_FOLIUM and features:
            print("\nCreating map visualization...")
            
            # Extract coordinates for the map
            coordinates = []
            for feature in features:
                if feature["geometry"]["type"] == "Point":
                    lon, lat = feature["geometry"]["coordinates"]
                    timestamp = feature["properties"].get("timestamp", "")
                    coordinates.append((lat, lon, timestamp))
            
            # Create a map centered on the first point
            first_lat, first_lon, _ = coordinates[0]
            m = folium.Map(location=[first_lat, first_lon], zoom_start=8)
            
            # Add a polyline for the vessel track
            points = [(lat, lon) for lat, lon, _ in coordinates]
            folium.PolyLine(
                points,
                color="blue",
                weight=2,
                opacity=0.7,
                popup=vessel_name
            ).add_to(m)
            
            # Add markers for start and end points
            folium.Marker(
                points[0],
                popup=f"Start: {coordinates[0][2]}",
                icon=folium.Icon(color="green")
            ).add_to(m)
            
            folium.Marker(
                points[-1],
                popup=f"End: {coordinates[-1][2]}",
                icon=folium.Icon(color="red")
            ).add_to(m)
            
            # Save the map to an HTML file
            map_file = "vessel_track.html"
            m.save(map_file)
            print(f"Map saved to {map_file}")
            
            # Try to open the map in a browser
            try:
                import webbrowser
                webbrowser.open('file://' + os.path.realpath(map_file))
            except:
                print(f"Please open {map_file} in your web browser to view the map")
        
        # Save raw track data to a JSON file for further analysis
        with open("track_data.json", "w") as f:
            json.dump(track_data, f, indent=2)
        print("Raw track data saved to track_data.json")
            
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        print("Track data may not be available for this vessel.")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
