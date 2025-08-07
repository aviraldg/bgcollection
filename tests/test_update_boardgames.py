import json
import unittest
from unittest.mock import patch, mock_open, MagicMock

from update_boardgames import (
    read_boardgames_data,
    write_boardgames_data,
    update_boardgames_data,
)


class TestUpdateBoardgames(unittest.TestCase):
    def test_read_boardgames_data_success(self):
        """Test reading a valid JSON file."""
        mock_data = json.dumps([{"title": "Game 1"}])
        with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
            data = read_boardgames_data("dummy_path.json")
            self.assertEqual(data, [{"title": "Game 1"}])
            mock_file.assert_called_once_with("dummy_path.json", "r")

    def test_read_boardgames_data_file_not_found(self):
        """Test reading a non-existent file."""
        with patch("builtins.open", side_effect=FileNotFoundError) as mock_file:
            data = read_boardgames_data("non_existent.json")
            self.assertIsNone(data)
            mock_file.assert_called_once_with("non_existent.json", "r")

    def test_read_boardgames_data_json_decode_error(self):
        """Test reading a file with invalid JSON."""
        with patch("builtins.open", mock_open(read_data="invalid json")) as mock_file:
            data = read_boardgames_data("invalid.json")
            self.assertIsNone(data)
            mock_file.assert_called_once_with("invalid.json", "r")

    def test_write_boardgames_data_success(self):
        """Test writing data to a file."""
        mock_data = [{"title": "Game 1"}]
        m = mock_open()
        with patch("builtins.open", m):
            result = write_boardgames_data("dummy_path.json", mock_data)
            self.assertTrue(result)
            m.assert_called_once_with("dummy_path.json", "w")
            handle = m()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertEqual(written_data, json.dumps(mock_data, indent=4))

    def test_write_boardgames_data_io_error(self):
        """Test handling an IOError during writing."""
        mock_data = [{"title": "Game 1"}]
        with patch("builtins.open", side_effect=IOError) as mock_file:
            result = write_boardgames_data("dummy_path.json", mock_data)
            self.assertFalse(result)
            mock_file.assert_called_once_with("dummy_path.json", "w")

    @patch("bgg_api.BggApi.get_bgg_game_details")
    def test_update_boardgames_data_success(self, mock_get_details):
        """Test updating board games data successfully."""
        mock_get_details.return_value = {
            "url": "http://bgg.com/1",
            "rank": 1,
            "score": 8.5,
            "min_players": 1,
            "max_players": 4,
            "min_playtime": 60,
            "max_playtime": 120,
            "weight": 3.5,
        }
        boardgames_data = [{"title": "Game 1"}]
        bgg_api = MagicMock()
        bgg_api.get_bgg_game_details.return_value = mock_get_details.return_value
        updated_count, updated_data = update_boardgames_data(boardgames_data, bgg_api)
        self.assertEqual(updated_count, 1)
        self.assertEqual(len(updated_data), 1)
        self.assertEqual(updated_data[0]["rank"], 1)
        bgg_api.get_bgg_game_details.assert_called_once_with("Game 1")

    @patch("bgg_api.BggApi.get_bgg_game_details")
    def test_update_boardgames_data_no_update_needed(self, mock_get_details):
        """Test that no update is performed if data is present."""
        boardgames_data = [
            {
                "title": "Game 1",
                "url": "http://bgg.com/1",
                "rank": 1,
                "score": 8.5,
                "min_players": 1,
                "max_players": 4,
                "min_playtime": 60,
                "max_playtime": 120,
                "weight": 3.5,
            }
        ]
        bgg_api = MagicMock()
        updated_count, updated_data = update_boardgames_data(boardgames_data, bgg_api)
        self.assertEqual(updated_count, 0)
        self.assertEqual(len(updated_data), 1)
        bgg_api.get_bgg_game_details.assert_not_called()

    @patch("bgg_api.BggApi.get_bgg_game_details")
    def test_update_boardgames_data_api_failure(self, mock_get_details):
        """Test handling of BGG API failure."""
        mock_get_details.return_value = None
        boardgames_data = [{"title": "Game 1"}]
        bgg_api = MagicMock()
        bgg_api.get_bgg_game_details.return_value = None
        updated_count, updated_data = update_boardgames_data(boardgames_data, bgg_api)
        self.assertEqual(updated_count, 0)
        self.assertEqual(len(updated_data), 1)
        self.assertEqual(updated_data[0]["rank"], "Not Found")
        self.assertEqual(bgg_api.get_bgg_game_details.call_count, 3)


    @patch("update_boardgames.write_boardgames_data")
    @patch("update_boardgames.update_boardgames_data")
    @patch("update_boardgames.read_boardgames_data")
    @patch("update_boardgames.BggApi")
    def test_main_success(
        self, mock_bgg_api, mock_read, mock_update, mock_write
    ):
        """Test the main function with successful execution."""
        mock_read.return_value = [{"title": "Game 1"}]
        mock_update.return_value = (1, [{"title": "Game 1", "rank": 1}])
        mock_write.return_value = True

        from update_boardgames import main

        main("dummy_path.json")

        mock_read.assert_called_once_with("dummy_path.json")
        mock_update.assert_called_once_with([{"title": "Game 1"}], mock_bgg_api.return_value)
        mock_write.assert_called_once_with("dummy_path.json", [{"title": "Game 1", "rank": 1}])


if __name__ == "__main__":
    unittest.main()
