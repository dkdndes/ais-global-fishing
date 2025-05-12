"""
AIS Global Fishing - A Python client for the Global Fishing Watch Gateway v3 API.

This package provides a simple interface to the Global Fishing Watch API,
allowing users to query vessel identity, AIS tracks, behavioral events,
port-visits, encounters, trips, risk scores & more.
"""

from .gfw_client_lib import GFWClient

__version__ = "0.1.0"
__author__ = "Peter Rosemann"
__email__ = "dkdndes@gmail.com"

__all__ = ["GFWClient"]
