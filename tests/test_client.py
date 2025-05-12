"""
Tests for the GFWClient class.
"""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import requests
from requests.exceptions import HTTPError

from ais_global_fishing import GFWClient


class TestGFWClient:
    """Test suite for the GFWClient class."""

    def test_init_with_explicit_api_key(self):
        """Test initialization with an explicit API key."""
        with patch("ais_global_fishing.gfw_client_lib.requests.Session") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            
            client = GFWClient(api_key="test_key")
            
            assert client.base_url == GFWClient.DEFAULT_BASE_URL
            mock_session.headers.update.assert_called_once_with({"Authorization": "Bearer test_key"})

    def test_init_with_env_api_key(self):
        """Test initialization with an API key from environment variables."""
        with patch("ais_global_fishing.gfw_client_lib.load_dotenv"), \
             patch("ais_global_fishing.gfw_client_lib.os.getenv", return_value="env_key"), \
             patch("ais_global_fishing.gfw_client_lib.requests.Session") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            
            client = GFWClient()
            
            mock_session.headers.update.assert_called_once_with({"Authorization": "Bearer env_key"})

    def test_init_no_api_key(self):
        """Test initialization with no API key raises ValueError."""
        with patch("ais_global_fishing.gfw_client_lib.load_dotenv"), \
             patch("ais_global_fishing.gfw_client_lib.os.getenv", return_value=None):
            
            with pytest.raises(ValueError, match="API key not found"):
                GFWClient()

    def test_get_success(self, client):
        """Test successful GET request."""
        client_obj, mock_session = client
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_session.get.return_value = mock_response
        
        result = client_obj._get("/test_path", {"param": "value"})
        
        mock_session.get.assert_called_once_with(
            f"{client_obj.base_url}/test_path", 
            params={"param": "value"}
        )
        assert result == {"data": "test_data"}

    def test_get_http_error(self, client):
        """Test GET request with HTTP error."""
        client_obj, mock_session = client
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        mock_session.get.return_value = mock_response
        
        with pytest.raises(HTTPError):
            client_obj._get("/test_path")

    def test_endpoint_exists_true(self, client):
        """Test _endpoint_exists when endpoint exists."""
        client_obj, mock_session = client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.head.return_value = mock_response
        
        result = client_obj._endpoint_exists("/test_path")
        
        mock_session.head.assert_called_once_with(
            f"{client_obj.base_url}/test_path", 
            allow_redirects=True
        )
        assert result is True

    def test_endpoint_exists_false(self, client):
        """Test _endpoint_exists when endpoint does not exist."""
        client_obj, mock_session = client
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session.head.return_value = mock_response
        
        result = client_obj._endpoint_exists("/test_path")
        
        assert result is False

    def test_search_vessels(self, client):
        """Test search_vessels method."""
        client_obj, mock_session = client
        expected_result = {"entries": [{"id": "vessel1"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        mock_session.get.return_value = mock_response
        
        result = client_obj.search_vessels(query="test_vessel", limit=5)
        
        mock_session.get.assert_called_once()
        # Check that the parameters were passed correctly
        call_args = mock_session.get.call_args
        params = call_args[1]['params']
        assert params['query'] == 'test_vessel'
        assert params['limit'] == 5
        assert result == expected_result

    def test_search_vessels_no_query_or_where(self, client):
        """Test search_vessels with no query or where raises ValueError."""
        client_obj, _ = client
        
        with pytest.raises(ValueError, match="Either 'query' or 'where' must be supplied"):
            client_obj.search_vessels()

    def test_get_vessel_details(self, client):
        """Test get_vessel_details method."""
        client_obj, mock_session = client
        expected_result = {"id": "vessel1", "name": "Test Vessel"}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        mock_session.get.return_value = mock_response
        
        result = client_obj.get_vessel_details(
            vessel_id="vessel1", 
            includes=["OWNERSHIP", "AUTHORIZATIONS"]
        )
        
        mock_session.get.assert_called_once()
        # Check that the URL contains the vessel ID
        call_args = mock_session.get.call_args
        assert "/vessels/vessel1" in call_args[0][0]
        # Check that the includes parameter was properly formatted
        params = call_args[1]['params']
        assert params['includes'] == 'OWNERSHIP,AUTHORIZATIONS'
        assert result == expected_result

    def test_get_track(self, client):
        """Test get_track method."""
        client_obj, mock_session = client
        mock_session.head.return_value.status_code = 200
        expected_result = {"tracks": [{"timestamp": "2023-01-01T00:00:00Z"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        mock_session.get.return_value = mock_response
        
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 31)
        
        result = client_obj.get_track(
            vessel_id="vessel1",
            start=start,
            end=end,
            resolution="2h"
        )
        
        assert mock_session.head.call_count == 1
        assert mock_session.get.call_count == 1
        # Check that the parameters were passed correctly
        call_args = mock_session.get.call_args
        params = call_args[1]['params']
        assert params['start'] == '2023-01-01T00:00:00Z'
        assert params['end'] == '2023-01-31T00:00:00Z'
        assert params['resolution'] == '2h'
        assert result == expected_result

    def test_get_track_endpoint_not_found(self, client):
        """Test get_track when endpoint does not exist."""
        client_obj, mock_session = client
        mock_session.head.return_value.status_code = 404
        
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 31)
        
        with pytest.raises(FileNotFoundError, match="Track endpoint not available"):
            client_obj.get_track(
                vessel_id="vessel1",
                start=start,
                end=end
            )
