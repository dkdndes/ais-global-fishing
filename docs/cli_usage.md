# Command Line Interface

The AIS Global Fishing package includes a command-line interface (CLI) for quick vessel searches and lookups without writing Python code.

## Installation

The CLI is automatically installed when you install the package:

```bash
# Using uv (recommended)
uv pip install -e .
# Then you can run the CLI with:
uv run gfw --help

# Or using pip
pip install -e .
# Then you can run the CLI directly:
gfw --help
```

> **Important**: When using `uv run gfw`, make sure you've installed the package in development mode with `uv pip install -e .` first.

## Basic Usage

### Getting Help

```bash
# Using uv
uv run gfw --help

# Or if installed in your active environment
gfw --help
```

This will display the available commands and options.

### Searching for Vessels

Search for vessels by name, MMSI, IMO, or other identifiers:

```bash
uv run gfw search "BOYANG"
```

You can also use the `--where` option for more complex queries:

```bash
uv run gfw search --where "flag = 'CHN' AND vesselType = 'FISHING'"
```

Additional options:
- `--limit`: Maximum number of results to return (default: 5)
- `--dataset`: Specify the dataset to search (default: public-global-vessel-identity:latest)

### Getting Vessel Details

Once you have a vessel ID, you can get detailed information:

```bash
uv run gfw details <vessel-id>
```

## Environment Variables

The CLI uses the same authentication methods as the Python library:

1. Set the `GLOBALFISHING_WATCH_API_KEY` environment variable
2. Create a `.env` file with your API key

## Examples

### Search for vessels with "TUNA" in their name:

```bash
uv run gfw search "TUNA" --limit 10
```

### Get details for a specific vessel:

```bash
uv run gfw details 123456789-abcdef0123456789
```

### Search for large fishing vessels:

```bash
uv run gfw search --where "vesselType = 'FISHING' AND length > 100"
```
