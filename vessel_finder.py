#!/usr/bin/env python3
import os
import requests
import pprint
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment variables
TOKEN = os.getenv('GLOBALFISHING_WATCH_API_KEY')
BASE = "https://gateway.api.globalfishingwatch.org/v3"
HEAD = {"Authorization": f"Bearer {TOKEN}"}

def find_vessel_by_mmsi(mmsi):
    """Find a vessel by MMSI number"""
    print(f"Searching for vessel with MMSI: {mmsi}")
    
    # 1) Find a vessel by MMSI
    search_params = {
        "query": mmsi,
        "datasets[0]": "public-global-vessel-identity:latest",
        "includes[0]": "MATCH_CRITERIA"
    }
    
    try:
        response = requests.get(f"{BASE}/vessels/search", params=search_params, headers=HEAD)
        response.raise_for_status()
        hit = response.json()
        
        if not hit.get("entries") or len(hit["entries"]) == 0:
            print(f"No vessels found with MMSI: {mmsi}")
            return None
        
        vessel_id = hit["entries"][0]["selfReportedInfo"][0]["id"]
        print(f"Found vessel with ID: {vessel_id}")
        
        # 2) Pull full identity record
        detail_params = {
            "dataset": "public-global-vessel-identity:latest",
            "includes[0]": "OWNERSHIP"
        }
        
        detail_response = requests.get(f"{BASE}/vessels/{vessel_id}", params=detail_params, headers=HEAD)
        detail_response.raise_for_status()
        detail = detail_response.json()
        
        return detail
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Example MMSI for "MISS FREYA"
    mmsi = "368045130"
    
    # Find vessel by MMSI
    vessel_detail = find_vessel_by_mmsi(mmsi)
    
    # Print vessel details
    if vessel_detail:
        print("\nVessel Details:")
        pprint.pp(vessel_detail)
