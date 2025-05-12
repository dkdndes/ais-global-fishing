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
#!/bin/bash
# Script to run all example files in the examples directory

echo "AIS Global Fishing - Running Examples"
echo "===================================="

# Check if the virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Warning: It's recommended to run examples in a virtual environment."
    echo "You can create one with: uv venv && source .venv/bin/activate"
    echo ""
fi

# Check for required dependencies
echo "Checking for dependencies..."
MISSING_DEPS=()

# Check for tabulate (used in several examples)
python -c "import tabulate" 2>/dev/null || MISSING_DEPS+=("tabulate")

# Check for matplotlib (used in bulk_vessels example)
python -c "import matplotlib" 2>/dev/null || MISSING_DEPS+=("matplotlib")

# Check for folium (used in track example)
python -c "import folium" 2>/dev/null || MISSING_DEPS+=("folium")

# Install missing dependencies if any
if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Some optional dependencies are missing: ${MISSING_DEPS[*]}"
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install ${MISSING_DEPS[*]}
    else
        echo "Some examples may not work correctly without these dependencies."
    fi
fi

# Run each example
echo -e "\nRunning examples...\n"

EXAMPLES=(
    "example_usage.py"
    "example_search_advanced.py"
    "example_track.py"
    "example_events.py"
    "example_port_visits.py"
    "example_bulk_vessels.py"
)

for example in "${EXAMPLES[@]}"; do
    if [ -f "examples/$example" ]; then
        echo -e "\n\n========== Running $example =========="
        python "examples/$example"
        echo -e "\n========== Finished $example ==========\n"
        
        # Pause between examples
        read -p "Press Enter to continue to the next example..." -n 1 -s
        echo
    else
        echo "Warning: Example file examples/$example not found"
    fi
done

echo -e "\nAll examples completed!"
