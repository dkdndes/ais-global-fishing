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

# Check if the package is installed in development mode
if ! uv run python -c "import ais_global_fishing" &>/dev/null; then
    echo "Installing package in development mode..."
    uv pip install -e .
fi

# Check for required dependencies
echo "Checking for dependencies..."
MISSING_DEPS=()

# Check for tabulate (used in several examples)
uv run -c "import tabulate" 2>/dev/null || MISSING_DEPS+=("tabulate")

# Check for matplotlib (used in bulk_vessels example)
uv run -c "import matplotlib" 2>/dev/null || MISSING_DEPS+=("matplotlib")

# Check for folium (used in track example)
uv run -c "import folium" 2>/dev/null || MISSING_DEPS+=("folium")

# Install missing dependencies if any
if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Some optional dependencies are missing: ${MISSING_DEPS[*]}"
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        uv pip install ${MISSING_DEPS[*]}
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
        uv run python "examples/$example"
        echo -e "\n========== Finished $example ==========\n"
        
        # Pause between examples
        read -p "Press Enter to continue to the next example..." -n 1 -s
        echo
    else
        echo "Warning: Example file examples/$example not found"
    fi
done

echo -e "\nAll examples completed!"
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
uv run -c "import tabulate" 2>/dev/null || MISSING_DEPS+=("tabulate")

# Check for matplotlib (used in bulk_vessels example)
uv run -c "import matplotlib" 2>/dev/null || MISSING_DEPS+=("matplotlib")

# Check for folium (used in track example)
uv run -c "import folium" 2>/dev/null || MISSING_DEPS+=("folium")

# Install missing dependencies if any
if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Some optional dependencies are missing: ${MISSING_DEPS[*]}"
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        uv pip install ${MISSING_DEPS[*]}
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
        uv run "examples/$example"
        echo -e "\n========== Finished $example ==========\n"
        
        # Pause between examples
        read -p "Press Enter to continue to the next example..." -n 1 -s
        echo
    else
        echo "Warning: Example file examples/$example not found"
    fi
done

echo -e "\nAll examples completed!"
