import unittest
from unittest.mock import patch, MagicMock

from update_collection import update_bgg_collection
from bgg_collection_manager import BggCollectionManager


class TestUpdateCollection(unittest.TestCase):
    @patch("bgg_collection_manager.BggCollectionManager.add_game_to_collection")
    def test_update_bgg_collection(self, mock_add_game):
        """Test the main loop for updating the collection."""
        collection_manager = MagicMock()
        boardgames_data = [{"title": "Game 1"}, {"title": "Game 2"}]
        update_bgg_collection(collection_manager, boardgames_data)
        self.assertEqual(collection_manager.add_game_to_collection.call_count, 2)
        collection_manager.add_game_to_collection.assert_any_call({"title": "Game 1"})
        collection_manager.add_game_to_collection.assert_any_call({"title": "Game 2"})

if __name__ == "__main__":
    unittest.main()
