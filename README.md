# AIS Global Fishing Wrapper Library

*A minimal yet powerful wrapper around the  
[Global Fishing Watch **Gateway v3** API](https://docs.globalfishingwatch.org/).*

This Python client library allows you to query vessel identity, AIS
tracks, behavioral events, port-visits, encounters, trips, risk scores & more
– all from concise, typed Python helpers.

## Installation

```bash
# Using pip
pip install git+https://github.com/dkdndes/ais-global-fishing.git

# Or install from source
git clone https://github.com/dkdndes/ais-global-fishing.git
cd ais-global-fishing
pip install -e .
```

## Authentication

You'll need an API key from Global Fishing Watch. Once you have it, you can:

### Option A: Use an environment variable

```bash
export GLOBALFISHING_WATCH_API_KEY="your-api-key-here"
```

Or create a `.env` file in your project directory:

```
GLOBALFISHING_WATCH_API_KEY=your-api-key-here
```

### Option B: Pass the API key directly

```python
from ais_global_fishing import GFWClient

client = GFWClient(api_key="your-api-key-here")
```

## Quick Start

```python
from ais_global_fishing import GFWClient
from datetime import datetime, timedelta

# Initialize the client
client = GFWClient()

# Search for vessels
results = client.search_vessels(query="BOYANG")

if results.get("entries"):
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

## Features

- Search vessels by MMSI, IMO, name, or custom queries
- Get detailed vessel information
- Retrieve AIS tracks with customizable resolution
- Access behavioral events (fishing, encounters, loitering, etc.)
- Get port visits, trips, and risk scores
- Fully typed API for better developer experience

## Examples

The package includes several example scripts in the `examples/` directory:

| Script                                   | What it shows                               |
| ---------------------------------------- | ------------------------------------------- |
| `examples/example_usage.py`              | End-to-end: search + details                |
| `examples/example_track.py`              | Recent 7-day AIS track                      |
| `examples/example_events.py`             | Behavioural events (fishing, port-visit)    |
| `examples/example_port_visits.py`        | Port calls in last year                     |
| `examples/example_bulk_vessels.py`       | Bulk identity lookup with extra parameters  |
| `examples/example_search_advanced.py`    | Flags, gear-types, binary responses         |

Run any example with:

```bash
python examples/example_usage.py
```

Or use the provided script:

```bash
./run_examples.sh example_usage
```

## Documentation

For more detailed documentation:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then visit http://127.0.0.1:8000/ in your browser.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Peter Rosemann ([@dkdndes](https://github.com/dkdndes))

