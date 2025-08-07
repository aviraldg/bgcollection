from file_utils import read_boardgames_data
from bgg_collection_manager import BggCollectionManager

JSON_FILE_PATH = "/home/aviraldg/Downloads/boardgames.json"


def update_bgg_collection(collection_manager, boardgames_data):
    """
    Iterates through the board games data and adds each game to the BGG collection.
    """
    for game in boardgames_data:
        collection_manager.add_game_to_collection(game)


def main():
    """
    Main function to update the BGG collection.
    """
    boardgames_data = read_boardgames_data(JSON_FILE_PATH)
    if boardgames_data is None:
        return

    collection_manager = BggCollectionManager()
    collection_manager.setup_driver()
    collection_manager.login_to_bgg()
    update_bgg_collection(collection_manager, boardgames_data)
    collection_manager.close_driver()
    print("Script finished. Check your BoardGameGeek collection.")


if __name__ == "__main__":
    main()
