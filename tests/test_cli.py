"""
Tests for the CLI functionality.
"""
import argparse
from unittest.mock import MagicMock, patch

import pytest

from ais_global_fishing.__main__ import build_parser, cmd_details, cmd_search, main


class TestCLI:
    """Test suite for the CLI functionality."""

    def test_build_parser(self):
        """Test that the parser is built correctly."""
        parser = build_parser()
        
        assert isinstance(parser, argparse.ArgumentParser)
        
        # Check that the subparsers are created
        subparsers = [action for action in parser._actions 
                     if isinstance(action, argparse._SubParsersAction)]
        assert len(subparsers) == 1
        
        # Check that the search and details subparsers exist
        subparser_choices = subparsers[0].choices
        assert "search" in subparser_choices
        assert "details" in subparser_choices

    def test_cmd_search_success(self, capsys):
        """Test successful search command."""
        mock_client = MagicMock()
        mock_client.search_vessels.return_value = {
            "entries": [{"id": "vessel1", "name": "Test Vessel"}]
        }
        
        with patch("ais_global_fishing.__main__.GFWClient", return_value=mock_client):
            args = argparse.Namespace(
                query="test_vessel",
                where=None,
                limit=5,
                include=["OWNERSHIP"],
                no_binary=True
            )
            
            cmd_search(args)
            
            captured = capsys.readouterr()
            assert "Found 1 entries" in captured.out
            assert "vessel1" in captured.out
            mock_client.search_vessels.assert_called_once_with(
                query="test_vessel",
                where=None,
                limit=5,
                datasets=["public-global-vessel-identity:latest"],
                includes=["OWNERSHIP"],
                binary=False
            )

    def test_cmd_search_no_results(self, capsys):
        """Test search command with no results."""
        mock_client = MagicMock()
        mock_client.search_vessels.return_value = {"entries": []}
        
        with patch("ais_global_fishing.__main__.GFWClient", return_value=mock_client), \
             patch("ais_global_fishing.__main__.sys.exit") as mock_exit:
            
            args = argparse.Namespace(
                query="nonexistent_vessel",
                where=None,
                limit=5,
                include=None,
                no_binary=False
            )
            
            cmd_search(args)
            
            captured = capsys.readouterr()
            assert "No vessels found" in captured.err
            mock_exit.assert_called_once_with(1)

    def test_cmd_details(self, capsys):
        """Test details command."""
        mock_client = MagicMock()
        mock_client.get_vessel_details.return_value = {
            "id": "vessel1", 
            "name": "Test Vessel"
        }
        
        with patch("ais_global_fishing.__main__.GFWClient", return_value=mock_client):
            args = argparse.Namespace(
                vessel_id="vessel1",
                include=["OWNERSHIP"]
            )
            
            cmd_details(args)
            
            captured = capsys.readouterr()
            assert "vessel1" in captured.out
            assert "Test Vessel" in captured.out
            mock_client.get_vessel_details.assert_called_once_with(
                vessel_id="vessel1",
                includes=["OWNERSHIP"]
            )

    def test_main(self):
        """Test the main function."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_parser.parse_args.return_value = mock_args
        
        with patch("ais_global_fishing.__main__.build_parser", return_value=mock_parser):
            main()
            
            mock_parser.parse_args.assert_called_once()
            mock_args.func.assert_called_once_with(mock_args)
