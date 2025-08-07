import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET

from bgg_api import BggApi


class TestBggApi(unittest.TestCase):
    def setUp(self):
        self.api = BggApi()

    @patch("bgg_api.requests.get")
    def test_search_game_success(self, mock_get):
        """Test a successful game search."""
        mock_response = MagicMock()
        mock_response.content = b'<items><item id="123"></item></items>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        game_ids = self.api.search_game("Test Game")
        self.assertEqual(game_ids, ["123"])
        mock_get.assert_called_once_with(
            "https://boardgamegeek.com/xmlapi2/search",
            params={"query": "Test Game", "type": "boardgame"},
        )

    @patch("bgg_api.requests.get")
    def test_search_game_no_results(self, mock_get):
        """Test a game search with no results."""
        mock_response = MagicMock()
        mock_response.content = b"<items></items>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        game_ids = self.api.search_game("Unknown Game")
        self.assertEqual(game_ids, [])

    @patch("bgg_api.requests.get")
    def test_get_game_details_success(self, mock_get):
        """Test getting game details successfully."""
        mock_response = MagicMock()
        mock_response.content = b'<items><item id="123"><name value="Test Game"/></item></items>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        game_details = self.api.get_game_details(["123"])
        self.assertEqual(len(game_details), 1)
        self.assertEqual(game_details[0]["id"], "123")

    @patch("bgg_api.BggApi.search_game")
    @patch("bgg_api.BggApi.get_game_details")
    def test_get_bgg_game_details_success(self, mock_get_details, mock_search):
        """Test the end-to-end process of getting game details."""
        mock_search.return_value = ["123"]
        mock_get_details.return_value = [
            {
                "id": "123",
                "rank": 1,
                "score": 8.5,
                "min_players": 1,
                "max_players": 4,
                "min_playtime": 60,
                "max_playtime": 120,
                "weight": 3.5,
            }
        ]

        details = self.api.get_bgg_game_details("Test Game")
        self.assertIsNotNone(details)
        self.assertEqual(details["rank"], 1)
        mock_search.assert_called_once_with("Test Game")
        mock_get_details.assert_called_once_with(["123"])


if __name__ == "__main__":
    unittest.main()
