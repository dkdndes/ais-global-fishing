#!/usr/bin/env python3
import os
import json
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

# Generate curl command
curl_command = f"""curl -X GET "{vessels_search_url}?{datasets_param}" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json"
"""

print("Generated curl command for vessels search:")
print(curl_command)

# You can add optional parameters like:
# - limit=20
# - query=your_search_term (min 3 characters)
# - includes[]=OWNERSHIP&includes[]=AUTHORIZATIONS
print("\nTo add optional parameters, append them to the URL in the curl command.")
print("Example with query parameter:")
query_example = f"""curl -X GET "{vessels_search_url}?{datasets_param}&query=Phoenix" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json"
"""
print(query_example)
