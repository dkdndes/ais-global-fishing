#!/usr/bin/env python3
import json
import argparse
from gfw_client import search_vessels

def main():
    """
    Command-line interface for searching vessels using the GFW API client
    """
    parser = argparse.ArgumentParser(description="Search for vessels using Global Fishing Watch API")
    parser.add_argument("--query", "-q", type=str, help="Search term (min 3 characters)")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Number of results to return (max 50)")
    parser.add_argument("--include-ownership", action="store_true", help="Include ownership information")
    parser.add_argument("--include-authorizations", action="store_true", help="Include authorization information")
    parser.add_argument("--include-match-criteria", action="store_true", help="Include match criteria information")
    parser.add_argument("--output", "-o", type=str, help="Output file for results (JSON format)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed information")
    
    args = parser.parse_args()
    
    # Prepare includes parameter
    includes = []
    if args.include_ownership:
        includes.append("OWNERSHIP")
    if args.include_authorizations:
        includes.append("AUTHORIZATIONS")
    if args.include_match_criteria:
        includes.append("MATCH_CRITERIA")
    
    # Search for vessels
    print(f"Searching for vessels{' with query: ' + args.query if args.query else ''}...")
    results = search_vessels(
        query=args.query,
        limit=args.limit,
        includes=includes if includes else None
    )
    
    # Process results
    entries = results.get('entries', [])
    print(f"Found {len(entries)} vessels")
    
    if args.verbose and entries:
        # Print first 5 results
        for i, vessel in enumerate(entries[:5]):
            print(f"\nVessel {i+1}:")
            print(f"  Name: {vessel.get('shipname', 'Unknown')}")
            print(f"  MMSI: {vessel.get('mmsi', 'Unknown')}")
            print(f"  IMO: {vessel.get('imo', 'Unknown')}")
            print(f"  Flag: {vessel.get('flag', 'Unknown')}")
            print(f"  Vessel type: {vessel.get('vesselType', 'Unknown')}")
    
    # Save to file if requested
    if args.output and entries:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
