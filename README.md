# AIS Global Fishing Wrapper Library

*A minimal yet powerful wrapper around the  
[Global Fishing Watch **Gateway v3** API](https://docs.globalfishingwatch.org/).*

This Python client library allows you to query vessel identity, AIS
tracks, behavioral events, port-visits, encounters, trips, risk scores & more
– all from concise, typed Python helpers.

## Installation

```bash
# Using uv (recommended)
uv install git+https://github.com/dkdndes/ais-global-fishing.git

# Or using pip
pip install git+https://github.com/dkdndes/ais-global-fishing.git
```

## Quick Start

1. Get your API token from [Global Fishing Watch](https://globalfishingwatch.org/)
2. Create a `.env` file with your token:
   ```
   GLOBALFISHING_WATCH_API_KEY=your_api_key_here
   ```
3. Start using the library:

```python
from ais_global_fishing import GFWClient

# Initialize the client
client = GFWClient()

# Search for vessels
vessels = client.search_vessels(query="368045130")

# Get vessel details
vessel_details = client.get_vessel_details(vessel_id="your-vessel-id")

# Get vessel tracks
from datetime import datetime
tracks = client.get_track(
    vessel_id="your-vessel-id",
    start=datetime(2022, 1, 1),
    end=datetime(2022, 1, 31)
)
```

## Features

- Search vessels by MMSI, IMO, name, or custom queries
- Get detailed vessel information
- Retrieve AIS tracks with customizable resolution
- Access behavioral events (fishing, encounters, loitering, etc.)
- Get port visits, trips, and risk scores
- Fully typed API for better developer experience

## CLI Tool

The package also includes a command-line interface:

```bash
# Search for a vessel
python -m ais_global_fishing search 368045130

# Get vessel details
python -m ais_global_fishing details your-vessel-id
```

## Documentation

For more detailed documentation, see the [docs](./docs) directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Peter Rosemann ([@dkdndes](https://github.com/dkdndes))

