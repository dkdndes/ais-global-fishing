"""
Test configuration and fixtures for the AIS Global Fishing library.
"""
import os
from unittest.mock import MagicMock, patch

import pytest
import requests

from ais_global_fishing import GFWClient


@pytest.fixture
def mock_response():
    """Create a mock response with customizable content."""
    mock = MagicMock()
    mock.status_code = 200
    mock.raise_for_status.return_value = None
    mock.json.return_value = {}
    return mock


@pytest.fixture
def mock_session():
    """Create a mock requests.Session with customizable behavior."""
    mock = MagicMock(spec=requests.Session)
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {}
    mock.head.return_value.status_code = 200
    return mock


@pytest.fixture
def client():
    """Create a GFWClient with a mocked API key."""
    with patch.dict(os.environ, {"GLOBALFISHING_WATCH_API_KEY": "test_api_key"}):
        with patch("ais_global_fishing.gfw_client_lib.requests.Session") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            client = GFWClient()
            yield client, mock_session
