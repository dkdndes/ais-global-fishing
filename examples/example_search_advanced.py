#!/usr/bin/env python3
"""
example_search_advanced.py

Demonstrate advanced search capabilities:
  • binary flag
  • `where` queries with gear-type, flag, etc.
  • extra includes
  • complex filtering and analysis
"""

from pprint import pprint
import json
from tabulate import tabulate
import os

from ais_global_fishing import GFWClient


def main():
    client = GFWClient()
    print("AIS Global Fishing - Advanced Search Examples")
    print("--------------------------------------------")

    # Example 1 ─ vessels flagged CHN (non-binary response)
    print("\n1. Searching for vessels flagged to China (CHN)...")
    res_flag = client.search_vessels(
        where="flag = 'CHN'",
        datasets=["public-global-vessel-identity:latest"],
        binary=False,
        limit=3,
    )
    print(f"Found {len(res_flag.get('entries', []))} Chinese vessels (showing first 3):")
    
    if res_flag.get('entries'):
        vessel_names = []
        for e in res_flag["entries"]:
            if e.get("registryInfo") and len(e["registryInfo"]) > 0:
                vessel_names.append(e["registryInfo"][0].get("shipname", "Unknown"))
            else:
                vessel_names.append(e.get("name", "Unknown"))
        pprint(vessel_names)
    else:
        print("No vessels found.")

    # Example 2 ─ purse-seine vessels
    print("\n2. Searching for tuna purse-seine vessels...")
    res_gear = client.search_vessels(
        where="geartypes='TUNA_PURSE_SEINES'",
        datasets=["public-global-vessel-identity:latest"],
        binary=False,
        limit=3,
    )
    print(f"Found {len(res_gear.get('entries', []))} tuna purse-seiners (showing first 3):")
    
    if res_gear.get('entries'):
        vessel_names = []
        for e in res_gear["entries"]:
            if e.get("registryInfo") and len(e["registryInfo"]) > 0:
                vessel_names.append(e["registryInfo"][0].get("shipname", "Unknown"))
            else:
                vessel_names.append(e.get("name", "Unknown"))
        pprint(vessel_names)
    else:
        print("No vessels found.")

    # Example 3 ─ query by IMO with extra includes
    print("\n3. Searching for vessel by IMO number with ownership information...")
    res_imo = client.search_vessels(
        query="9111694",
        datasets=["public-global-vessel-identity:latest"],
        includes=["MATCH_CRITERIA", "OWNERSHIP"],
        limit=1,
    )
    
    if res_imo.get('entries'):
        print("Found vessel with ownership information:")
        vessel = res_imo["entries"][0]
        
        # Extract and display key information in a more readable format
        vessel_info = {
            "Name": vessel.get("name", "Unknown"),
            "IMO": vessel.get("imo", "Unknown"),
            "MMSI": vessel.get("mmsi", "Unknown"),
            "Flag": vessel.get("flagState", "Unknown"),
            "Vessel Type": vessel.get("vesselType", "Unknown")
        }
        
        # Extract ownership information if available
        if "ownership" in vessel:
            owners = []
            for owner in vessel["ownership"]:
                owner_info = {
                    "Owner": owner.get("owner", "Unknown"),
                    "Owner Type": owner.get("ownerType", "Unknown"),
                    "Country": owner.get("country", "Unknown")
                }
                owners.append(owner_info)
            
            print("\nVessel Information:")
            print(tabulate([vessel_info.values()], headers=vessel_info.keys(), tablefmt="grid"))
            
            print("\nOwnership Information:")
            if owners:
                print(tabulate([o.values() for o in owners], headers=owners[0].keys(), tablefmt="grid"))
            else:
                print("No detailed ownership information available.")
        else:
            print("No ownership information available.")
            print("\nVessel Information:")
            print(tabulate([vessel_info.values()], headers=vessel_info.keys(), tablefmt="grid"))
        
        # Save the full vessel data to a JSON file for further analysis
        with open("vessel_details.json", "w") as f:
            json.dump(vessel, f, indent=2)
        print("\nFull vessel details saved to vessel_details.json")
    else:
        print("No vessel found with this IMO number.")

    # Example 4 - Combined complex query
    print("\n4. Complex query: Large fishing vessels (>24m) with high seas authorization...")
    complex_query = client.search_vessels(
        where="vesselType = 'FISHING' AND length > 24 AND authorizations IS NOT NULL",
        datasets=["public-global-vessel-identity:latest"],
        binary=False,
        limit=5,
    )
    
    print(f"Found {len(complex_query.get('entries', []))} vessels matching criteria (showing first 5):")
    
    if complex_query.get('entries'):
        # Create a table with key vessel information
        table_data = []
        headers = ["Name", "Flag", "Length", "Vessel Type", "Authorizations"]
        
        for vessel in complex_query["entries"]:
            auth_count = len(vessel.get("authorizations", []))
            row = [
                vessel.get("name", "Unknown"),
                vessel.get("flagState", "Unknown"),
                vessel.get("length", "Unknown"),
                vessel.get("vesselType", "Unknown"),
                f"{auth_count} authorization(s)"
            ]
            table_data.append(row)
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("No vessels found matching these criteria.")


if __name__ == "__main__":
    main()
