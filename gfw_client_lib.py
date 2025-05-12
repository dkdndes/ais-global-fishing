#!/usr/bin/env python3
"""
gfw_client_lib.py

A client library for Global Fishing Watch API.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv


class GFWClient:
    """Client for the Global Fishing Watch API."""

    DEFAULT_BASE_URL = "https://gateway.api.globalfishingwatch.org/v3"

    def __init__(self, api_key=None, base_url=None):
        """
        Initialize the client.

        Parameters:
            api_key (str): API key for authentication. If not provided, read from GLOBALFISHING_WATCH_API_KEY
                           env var or .env file.
            base_url (str): Base URL for the API.
        """
        if not api_key:
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)
            api_key = os.getenv('GLOBALFISHING_WATCH_API_KEY')
        if not api_key:
            raise ValueError("API key must be provided via parameter or environment variable.")
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    # --------------------------------------------------------------------- #
    #  VESSEL SEARCH
    # --------------------------------------------------------------------- #
    def search_vessels(
        self,
        query,
        datasets=None,
        includes=None,
        limit=20,
        match_fields=None,
    ):
        """
        Search for vessels by query (e.g., MMSI or IMO).

        Parameters
        ----------
        query : str
            Search term.
        datasets : list[str] | None
            Dataset IDs to search in, e.g. ['public-global-vessel-identity:latest'].
        includes : list[str] | None
            Extra sections to include in the response.  Valid values include
            'MATCH_CRITERIA', 'OWNERSHIP', etc.
        limit : int
            Maximum number of results to return.
        match_fields : str | None
            Filter by match fields, e.g. 'SEVERAL_FIELDS'.

        Returns
        -------
        dict
            Parsed JSON response.
        """
        params = {"query": query, "limit": limit}

        # datasets[] MUST be provided as indexed parameters
        if datasets:
            for idx, ds in enumerate(datasets):
                params[f"datasets[{idx}]"] = ds

        # NOTE: the *search* endpoint expects indexed includes parameters
        #       (e.g. includes[0]=MATCH_CRITERIA).  Sending a single
        #       comma-separated string triggers a 422 validation error.
        if includes:
            for idx, inc in enumerate(includes):
                params[f"includes[{idx}]"] = inc

        if match_fields:
            params["match_fields"] = match_fields

        response = self.session.get(f"{self.base_url}/vessels/search", params=params)
        response.raise_for_status()
        return response.json()

    # --------------------------------------------------------------------- #
    #  VESSEL DETAILS
    # --------------------------------------------------------------------- #
    def get_vessel_details(
        self,
        vessel_id,
        dataset="public-global-vessel-identity:latest",
        includes=None,
    ):
        """
        Retrieve a detailed vessel identity record.

        Parameters
        ----------
        vessel_id : str
            Vessel ID returned by the search endpoint.
        dataset : str
            Dataset version.  Defaults to 'public-global-vessel-identity:latest'.
        includes : list[str] | None
            Extra sections to include in the response.  Valid values include
            'OWNERSHIP', 'FLAG', etc.

        Returns
        -------
        dict
            Parsed JSON response.
        """
        params = {"dataset": dataset}

        # Contrary to the search endpoint, the *details* endpoint expects
        # a single, comma-separated string for the includes parameter.
        if includes:
            params["includes"] = ",".join(includes)

        response = self.session.get(f"{self.base_url}/vessels/{vessel_id}", params=params)
        response.raise_for_status()
        return response.json()
