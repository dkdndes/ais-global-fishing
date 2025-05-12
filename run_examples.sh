#!/bin/bash

# Check if API key is provided
if [ -z "$AISSTREAM_API_KEY" ]; then
    echo "Error: AISSTREAM_API_KEY environment variable is not set"
    echo "Please set it with: export AISSTREAM_API_KEY=your_api_key"
    exit 1
fi

# Install the package in development mode using uv
uv pip install -e .

# Run the examples
echo "Choose an example to run:"
echo "1. Basic AIS Stream Receiver"
echo "2. Ship Tracker"
echo "3. Message Statistics"
echo "4. Vessel Tracker with GeoJSON Output"
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Running Basic AIS Stream Receiver..."
        uv run -m ais_stream_lib.main
        ;;
    2)
        echo "Running Ship Tracker..."
        uv run -m ais_stream_lib.examples.ship_tracker
        ;;
    3)
        echo "Running Message Statistics..."
        uv run -m ais_stream_lib.examples.message_statistics --print-interval 5
        ;;
    4)
        echo "Running Vessel Tracker with GeoJSON Output..."
        uv run -m ais_stream_lib.examples.vessel_tracker_geojson --update-interval 10
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
