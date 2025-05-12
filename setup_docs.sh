#!/bin/bash
# Script to set up the environment and build the documentation

echo "Setting up environment for documentation..."

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source .venv/bin/activate

# Install the package with documentation dependencies
echo "Installing package with documentation dependencies..."
uv pip install -e ".[docs]"

# Build the documentation
echo "Building documentation..."
uv run mkdocs build

# Serve the documentation
echo "Starting documentation server..."
echo "View the documentation at http://127.0.0.1:8000/"
uv run mkdocs serve
