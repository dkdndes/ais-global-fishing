#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

# Try to import the GFW API client
try:
    from gfwapiclient import GFWClient
    from gfwapiclient.resources.vessels import VesselsResource
    HAS_GFW_CLIENT = True
except ImportError:
    HAS_GFW_CLIENT = False
    print("GFW API client not installed. Using direct API calls instead.")
    print("To install: uv add gfw-api-python-client")

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment variables
api_key = os.getenv('GLOBALFISHING_WATCH_API_KEY')

def search_vessels_with_client(query=None, limit=20, includes=None, match_fields=None):
    """
    Search vessels using the GFW API client library
    
    Args:
        query (str, optional): Search term (min 3 characters)
        limit (int, optional): Number of results to return (max 50)
        includes (list, optional): Extra information to include (OWNERSHIP, AUTHORIZATIONS, MATCH_CRITERIA)
        match_fields (list, optional): Filter by match fields (SEVERAL_FIELDS, NO_MATCH, ALL)
    
    Returns:
        dict: API response
    """
    if not HAS_GFW_CLIENT:
        raise ImportError("GFW API client not installed. Please install with: uv pip install gfw-api-python-client")
    
    if not api_key:
        raise ValueError("Missing GLOBALFISHING_WATCH_API_KEY environment variable")
    
    # Initialize the GFW client
    client = GFWClient(token=api_key)
    
    # Get the vessels resource
    vessels = VesselsResource(client)
    
    # Prepare parameters
    params = {
        "datasets": ["public-global-fishing-vessels:v2", "public-global-carrier-vessels:v2"],
        "limit": min(limit, 50)  # Maximum 50
    }
    
    # Add optional parameters
    if query and len(query) >= 3:
        params["query"] = query
    
    if includes:
        params["includes"] = includes
    
    if match_fields:
        params["match_fields"] = match_fields
    
    # Make the request
    try:
        # Search for vessels
        response = vessels.search(**params)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    if HAS_GFW_CLIENT:
        print("Searching vessels with GFW API client...")
        
        # Basic search
        results = search_vessels_with_client()
        print(f"\nFound {len(results.get('entries', []))} vessels")
        
        # Search with query
        query_results = search_vessels_with_client(query="Phoenix")
        print(f"\nFound {len(query_results.get('entries', []))} vessels matching 'Phoenix'")
        
        # Print first result if available
        if query_results.get('entries') and len(query_results.get('entries')) > 0:
            first_vessel = query_results['entries'][0]
            print("\nFirst vessel details:")
            import json
            print(json.dumps(first_vessel, indent=2))
    else:
        print("Please install the GFW API client to use this script:")
        print("uv add gfw-api-python-client")
