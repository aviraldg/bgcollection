import unittest
from unittest.mock import patch, MagicMock

from bgg_collection_manager import BggCollectionManager


class TestBggCollectionManager(unittest.TestCase):
    def setUp(self):
        self.manager = BggCollectionManager()
        self.manager.driver = MagicMock()

    @patch("bgg_collection_manager.Service")
    @patch("bgg_collection_manager.webdriver.Chrome")
    def test_setup_driver(self, mock_chrome, mock_service):
        """Test setting up the Chrome WebDriver."""
        manager = BggCollectionManager()
        manager.setup_driver()
        mock_service.assert_called_once()
        mock_chrome.assert_called_once()
        self.assertIsNotNone(manager.driver)

    @patch("builtins.input", return_value=None)
    def test_login_to_bgg(self, mock_input):
        """Test the login process."""
        self.manager.login_to_bgg()
        mock_input.assert_called_once()

    @patch("bgg_collection_manager.WebDriverWait")
    @patch("bgg_collection_manager.EC")
    def test_add_game_to_collection_success(self, mock_ec, mock_wait):
        """Test adding a game to the collection successfully."""
        game = {
            "title": "Test Game",
            "url": "https://boardgamegeek.com/boardgame/123",
        }

        # Mock the owned status link to not be found
        self.manager.driver.find_element.side_effect = Exception("Element not found")

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

        self.manager.add_game_to_collection(game)

        self.manager.driver.get.assert_called_once_with(
            "https://boardgamegeek.com/boardgame/123"
        )
        self.assertEqual(mock_add_button.click.call_count, 1)
        self.assertEqual(mock_owned_checkbox.click.call_count, 1)
        self.assertEqual(mock_save_button.click.call_count, 1)

    def test_add_game_to_collection_no_url(self):
        """Test skipping a game with no URL."""
        game = {"title": "Test Game"}
        self.manager.add_game_to_collection(game)
        self.manager.driver.get.assert_not_called()

    def test_add_game_to_collection_invalid_url(self):
        """Test skipping a game with an invalid URL."""
        game = {"title": "Test Game", "url": "invalid_url"}
        self.manager.add_game_to_collection(game)
        self.manager.driver.get.assert_not_called()

    def test_add_game_to_collection_already_owned(self):
        """Test skipping a game that is already owned."""
        game = {
            "title": "Test Game",
            "url": "https://boardgamegeek.com/boardgame/123",
        }

        # Mock the owned status link to be found
        mock_owned_link = MagicMock()
        mock_owned_link.is_displayed.return_value = True
        self.manager.driver.find_element.return_value = mock_owned_link

        self.manager.add_game_to_collection(game)

        self.manager.driver.get.assert_called_once_with(
            "https://boardgamegeek.com/boardgame/123"
        )
        self.manager.driver.find_element.assert_called_once()

    def test_close_driver(self):
        """Test closing the WebDriver."""
        self.manager.close_driver()
        self.manager.driver.quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
