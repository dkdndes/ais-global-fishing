#!/usr/bin/env python3
"""
gfw_client_lib.py

Thin Python wrapper around the Global Fishing Watch Gateway v3 API.
Only the most common endpoints are implemented; each method returns the
parsed JSON response (i.e. dict / list) or raises ``requests.HTTPError`` on
non-2xx status codes.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

import requests
from dotenv import load_dotenv


class GFWClient:
    """Client for the Global Fishing Watch Gateway v3 API."""

    DEFAULT_BASE_URL = "https://gateway.api.globalfishingwatch.org/v3"

    # ------------------------------------------------------------------ #
    # Construction / helpers
    # ------------------------------------------------------------------ #
    def __init__(self, api_key: Optional[str] = None, base_url: str | None = None):
        """
        Parameters
        ----------
        api_key
            API token.  If *None*, it is read from the ``GLOBALFISHING_WATCH_API_KEY``
            environment variable (``.env`` is loaded automatically).
        base_url
            Override API base (mostly useful for testing/staging).
        """
        if api_key is None:
            env_path = Path(".") / ".env"
            load_dotenv(env_path)
            api_key = os.getenv("GLOBALFISHING_WATCH_API_KEY")

        if not api_key:
            raise ValueError(
                "API key not found. "
                "Pass it explicitly or set GLOBALFISHING_WATCH_API_KEY / .env."
            )

        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    # Internal helper --------------------------------------------------- #
    def _get(self, path: str, params: dict | None = None):
        """Perform a GET request and return parsed JSON."""
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params or {})
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------ #
    # Search & identity endpoints
    # ------------------------------------------------------------------ #
    def search_vessels(
        self,
        query: str,
        datasets: Optional[Iterable[str]] = None,
        includes: Optional[Iterable[str]] = None,
        limit: int = 20,
        match_fields: Optional[str] = None,
    ):
        """
        Search for vessels (MMSI, IMO, name…).

        The search endpoint expects **indexed** params for lists,
        e.g. ``includes[0]=MATCH_CRITERIA``.
        """
        params: dict[str, str | int] = {"query": query, "limit": limit}

        if datasets:
            for idx, ds in enumerate(datasets):
                params[f"datasets[{idx}]"] = ds

        if includes:
            for idx, inc in enumerate(includes):
                params[f"includes[{idx}]"] = inc

        if match_fields:
            params["match_fields"] = match_fields

        return self._get("/vessels/search", params)

    def get_vessel_details(
        self,
        vessel_id: str,
        dataset: str = "public-global-vessel-identity:latest",
        includes: Optional[Iterable[str]] = None,
    ):
        """
        Retrieve full vessel identity.

        ``includes`` must be a comma-separated string for *this* endpoint.
        """
        params: dict[str, str] = {"dataset": dataset}

        if includes:
            params["includes"] = ",".join(includes)

        return self._get(f"/vessels/{vessel_id}", params)

    # ------------------------------------------------------------------ #
    # Track & trajectory
    # ------------------------------------------------------------------ #
    def get_track(
        self,
        vessel_id: str,
        start: datetime,
        end: datetime,
        resolution: str = "1h",
    ):
        """
        AIS track of a vessel.

        Parameters
        ----------
        start, end : datetime
            Time window (UTC).
        resolution : str
            E.g. ``5m``, ``1h``.
        """
        params = {
            "start": start.isoformat(timespec="seconds") + "Z",
            "end": end.isoformat(timespec="seconds") + "Z",
            "resolution": resolution,
        }
        return self._get(f"/vessels/{vessel_id}/track", params)

    def get_segments(
        self,
        vessel_id: str,
        start: datetime,
        end: datetime,
    ):
        """Continuous-signal trajectory segments."""
        params = {
            "start": start.isoformat(timespec="seconds") + "Z",
            "end": end.isoformat(timespec="seconds") + "Z",
        }
        return self._get(f"/vessels/{vessel_id}/segments", params)

    # ------------------------------------------------------------------ #
    # Behavioural events
    # ------------------------------------------------------------------ #
    def get_events(
        self,
        vessel_id: str,
        start: datetime,
        end: datetime,
        event_types: Optional[Iterable[str]] = None,
    ):
        """
        Events detected for *one* vessel.

        ``event_types`` can be a list such as ``["FISHING", "PORT_VISIT"]``.
        """
        params = {
            "start": start.isoformat(timespec="seconds") + "Z",
            "end": end.isoformat(timespec="seconds") + "Z",
        }
        if event_types:
            params["eventType"] = ",".join(event_types)
        return self._get(f"/vessels/{vessel_id}/events", params)

    # ---- mass event endpoints (encounters, transshipments, …) --------- #
    def _get_event_collection(
        self,
        collection_name: str,
        start: datetime,
        end: datetime,
        vessel_ids: Optional[Iterable[str]] = None,
    ):
        params = {
            "start": start.isoformat(timespec="seconds") + "Z",
            "end": end.isoformat(timespec="seconds") + "Z",
        }
        if vessel_ids:
            params["vesselIds"] = ",".join(vessel_ids)
        return self._get(f"/events/{collection_name}", params)

    def get_encounters(
        self, start: datetime, end: datetime, vessel_ids: Optional[Iterable[str]] = None
    ):
        """Buque-buque encounters (possible transhipment rendez-vous)."""
        return self._get_event_collection("encounters", start, end, vessel_ids)

    def get_transshipments(
        self, start: datetime, end: datetime, vessel_ids: Optional[Iterable[str]] = None
    ):
        """Confirmed / likely transhipment events."""
        return self._get_event_collection("transshipments", start, end, vessel_ids)

    def get_fishing_events(
        self, start: datetime, end: datetime, vessel_ids: Optional[Iterable[str]] = None
    ):
        """Fishing activity events."""
        return self._get_event_collection("fishing", start, end, vessel_ids)

    def get_loitering_events(
        self, start: datetime, end: datetime, vessel_ids: Optional[Iterable[str]] = None
    ):
        """Loitering events (slow movement in high-risk areas, etc.)."""
        return self._get_event_collection("loitering", start, end, vessel_ids)

    # ------------------------------------------------------------------ #
    # Ports / visits
    # ------------------------------------------------------------------ #
    def get_port_visits(
        self,
        start: datetime,
        end: datetime,
        vessel_ids: Optional[Iterable[str]] = None,
        port_ids: Optional[Iterable[str]] = None,
    ):
        params = {
            "start": start.isoformat(timespec="seconds") + "Z",
            "end": end.isoformat(timespec="seconds") + "Z",
        }
        if vessel_ids:
            params["vesselIds"] = ",".join(vessel_ids)
        if port_ids:
            params["portIds"] = ",".join(port_ids)
        return self._get("/ports/visits", params)

    # ------------------------------------------------------------------ #
    # Risk & compliance
    # ------------------------------------------------------------------ #
    def get_risk(self, vessel_id: str):
        """Compliance / IUU-risk scores (requires proper permissions)."""
        return self._get(f"/vessels/{vessel_id}/risk")

    # ------------------------------------------------------------------ #
    # Trips
    # ------------------------------------------------------------------ #
    def get_trips(self, vessel_id: str):
        """Port-to-port trips detected for *vessel_id*."""
        return self._get(f"/vessels/{vessel_id}/trips")
