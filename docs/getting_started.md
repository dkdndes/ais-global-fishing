# Getting Started

## Prerequisites

- Python 3.12 or higher
- A Global Fishing Watch API key

## Installation

Install the package using uv:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
# .venv\Scripts\activate  # On Windows

# Install the package
uv pip install git+https://github.com/dkdndes/ais-global-fishing.git
```

Or install from source:

```bash
git clone https://github.com/dkdndes/ais-global-fishing.git
cd ais-global-fishing
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -e .
```

## Setting up your API key

To use the Global Fishing Watch API, you need an API key. You can obtain one by registering at [Global Fishing Watch](https://globalfishingwatch.org/).

Once you have your API key, you can set it up in one of two ways:

### 1. Environment variable

Set the `GLOBALFISHING_WATCH_API_KEY` environment variable:

```bash
export GLOBALFISHING_WATCH_API_KEY="your-api-key-here"
```

Or create a `.env` file in your project directory:

```
GLOBALFISHING_WATCH_API_KEY=your-api-key-here
```

### 2. Pass directly to the client

```python
from ais_global_fishing import GFWClient

client = GFWClient(api_key="your-api-key-here")
```

## Basic Example

Here's a simple example to get you started:

```python
from ais_global_fishing import GFWClient
from datetime import datetime, timedelta

# Initialize the client
client = GFWClient()  # API key from environment or .env file

# Search for vessels
results = client.search_vessels(query="BOYANG")

if results.get("entries"):
    # Get the first vessel
    vessel = results["entries"][0]
    vessel_id = vessel["id"]
    
    print(f"Found vessel: {vessel['name']} (ID: {vessel_id})")
    
    # Get vessel details
    details = client.get_vessel_details(vessel_id)
    
    # Get recent track
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    try:
        track = client.get_track(vessel_id, start=start_date, end=end_date)
        print(f"Retrieved {len(track['features'])} track points")
    except FileNotFoundError:
        print("Track data not available for this vessel")
```

For more examples, see the [Examples](examples.md) page.
