import unittest
from unittest.mock import patch, MagicMock

from update_collection import update_bgg_collection
from bgg_collection_manager import add_game_to_collection


class TestUpdateCollection(unittest.TestCase):
    @patch("update_collection.add_game_to_collection")
    def test_update_bgg_collection(self, mock_add_game):
        """Test the main loop for updating the collection."""
        mock_driver = MagicMock()
        boardgames_data = [{"title": "Game 1"}, {"title": "Game 2"}]
        update_bgg_collection(mock_driver, boardgames_data)
        self.assertEqual(mock_add_game.call_count, 2)
        mock_add_game.assert_any_call(mock_driver, {"title": "Game 1"})
        mock_add_game.assert_any_call(mock_driver, {"title": "Game 2"})

    @patch("bgg_collection_manager.WebDriverWait")
    @patch("bgg_collection_manager.EC")
    def test_add_game_to_collection_success(self, mock_ec, mock_wait):
        """Test adding a game to the collection successfully."""
        mock_driver = MagicMock()
        game = {
            "title": "Test Game",
            "url": "https://boardgamegeek.com/boardgame/123",
        }

        # Mock the owned status link to not be found
        mock_driver.find_element.side_effect = Exception("Element not found")

        # Mock the "Add to Collection" button
        mock_add_button = MagicMock()
        mock_wait.return_value.until.return_value = mock_add_button

        # Mock the "Owned" checkbox and "Save" button
        mock_owned_checkbox = MagicMock()
        mock_owned_checkbox.is_selected.return_value = False
        mock_save_button = MagicMock()

        mock_wait.return_value.until.side_effect = [
            mock_add_button,
            mock_owned_checkbox,
            mock_save_button,
        ]

        add_game_to_collection(mock_driver, game)

        mock_driver.get.assert_called_once_with(
            "https://boardgamegeek.com/boardgame/123"
        )
        self.assertEqual(mock_add_button.click.call_count, 1)
        self.assertEqual(mock_owned_checkbox.click.call_count, 1)
        self.assertEqual(mock_save_button.click.call_count, 1)

    def test_add_game_to_collection_no_url(self):
        """Test skipping a game with no URL."""
        mock_driver = MagicMock()
        game = {"title": "Test Game"}
        add_game_to_collection(mock_driver, game)
        mock_driver.get.assert_not_called()

    def test_add_game_to_collection_invalid_url(self):
        """Test skipping a game with an invalid URL."""
        mock_driver = MagicMock()
        game = {"title": "Test Game", "url": "invalid_url"}
        add_game_to_collection(mock_driver, game)
        mock_driver.get.assert_not_called()

    def test_add_game_to_collection_already_owned(self):
        """Test skipping a game that is already owned."""
        mock_driver = MagicMock()
        game = {
            "title": "Test Game",
            "url": "https://boardgamegeek.com/boardgame/123",
        }

        # Mock the owned status link to be found
        mock_owned_link = MagicMock()
        mock_owned_link.is_displayed.return_value = True
        mock_driver.find_element.return_value = mock_owned_link

        add_game_to_collection(mock_driver, game)

        mock_driver.get.assert_called_once_with(
            "https://boardgamegeek.com/boardgame/123"
        )
        mock_driver.find_element.assert_called_once()


if __name__ == "__main__":
    unittest.main()
