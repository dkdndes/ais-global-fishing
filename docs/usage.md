# Quick-start

## 1 · Installation

```bash
# Using uv (recommended)
uv pip install git+https://github.com/dkdndes/ais-global-fishing.git

# Or install from source
git clone https://github.com/dkdndes/ais-global-fishing.git
cd ais-global-fishing
uv venv  # Create a virtual environment
source .venv/bin/activate  # On macOS/Linux
uv pip install -e .
```

## 2 · Authentication

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

## 3 · Basic Usage

### Search for vessels

```python
from ais_global_fishing import GFWClient

client = GFWClient()

# Search by name, MMSI, IMO, or callsign
results = client.search_vessels(query="BOYANG")

# Print the first result
if results.get("entries"):
    vessel = results["entries"][0]
    print(f"Found vessel: {vessel['name']} (ID: {vessel['id']})")
```

### Get vessel details

```python
# Get detailed information about a specific vessel
vessel_id = "123456789-123456789"  # Use an ID from search results
details = client.get_vessel_details(vessel_id)
print(f"Vessel details: {details['name']}, Flag: {details['flagState']}")
```

### Get vessel track

```python
from datetime import datetime, timedelta

# Get the vessel's track for the last 7 days
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

track = client.get_track(vessel_id, start=start_date, end=end_date)
print(f"Retrieved {len(track['features'])} track points")
```

### Get vessel events

```python
from datetime import datetime, timedelta

# Get events for the last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

events = client.get_events(
    vessel_id=vessel_id,
    start=start_date,
    end=end_date,
    event_types=["FISHING", "PORT_VISIT"]
)
print(f"Retrieved {len(events.get('entries', []))} events")
```

See the [Examples](examples.md) page for more advanced usage scenarios.

