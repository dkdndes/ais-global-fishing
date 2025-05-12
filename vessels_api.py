#!/usr/bin/env python3
import os
import json
import httpx
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key and base URL from environment variables
api_key = os.getenv('GLOBALFISHING_WATCH_API_KEY')
base_url = os.getenv('GLOBALFISHING_WATCH_BASE_URL')

if not api_key or not base_url:
    print("Error: Missing required environment variables.")
    exit(1)

# Remove trailing slash from base URL if present
base_url = base_url.rstrip('/')

# Construct the vessels search URL
vessels_search_url = f"{base_url}/v3/vessels/search"

# Required datasets parameter
datasets = ['public-global-fishing-vessels:latest', 'public-global-carrier-vessels:latest']
datasets_param = "&".join([f"datasets[]={dataset}" for dataset in datasets])

# Function to make API request using httpx
def search_vessels(query=None, limit=20, includes=None, match_fields=None):
    """
    Search vessels using the Global Fishing Watch API
    
    Args:
        query (str, optional): Search term (min 3 characters)
        limit (int, optional): Number of results to return (max 50)
        includes (list, optional): Extra information to include (OWNERSHIP, AUTHORIZATIONS, MATCH_CRITERIA)
        match_fields (list, optional): Filter by match fields (SEVERAL_FIELDS, NO_MATCH, ALL)
    
    Returns:
        dict: API response
    """
    # Build query parameters
    params = {}
    
    # Add datasets (required) - using the format datasets[]=value
    for i, dataset in enumerate(datasets):
        params[f'datasets[{i}]'] = dataset
    
    # Add optional parameters
    if query and len(query) >= 3:
        params['query'] = query
    
    if limit:
        params['limit'] = min(limit, 50)  # Maximum 50
    
    if includes:
        for include in includes:
            params.setdefault('includes[]', []).append(include)
    
    if match_fields:
        for field in match_fields:
            params.setdefault('match-fields[]', []).append(field)
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Make the request
    try:
        with httpx.Client() as client:
            response = client.get(vessels_search_url, params=params, headers=headers)
            print(f"Request URL: {response.url}")
            print(f"Request Headers: {headers}")
            
            if response.status_code != 200:
                print(f"Response Status: {response.status_code}")
                print(f"Response Body: {response.text}")
                
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
        return {"error": str(e)}
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    print("Searching vessels with Global Fishing Watch API...")
    
    # Basic search
    results = search_vessels()
    print(f"\nFound {len(results.get('entries', []))} vessels")
    
    # Search with query
    query_results = search_vessels(query="Phoenix")
    print(f"\nFound {len(query_results.get('entries', []))} vessels matching 'Phoenix'")
    
    # Print first result if available
    if query_results.get('entries') and len(query_results.get('entries')) > 0:
        first_vessel = query_results['entries'][0]
        print("\nFirst vessel details:")
        print(json.dumps(first_vessel, indent=2))
