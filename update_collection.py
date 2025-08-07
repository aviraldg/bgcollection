import sys
from file_utils import read_boardgames_data
from bgg_collection_manager import setup_driver, login_to_bgg, add_game_to_collection

JSON_FILE_PATH = "/home/aviraldg/Downloads/boardgames.json"


def update_bgg_collection(driver, boardgames_data):
    """
    Iterates through the board games data and adds each game to the BGG collection.
    """
    for game in boardgames_data:
        add_game_to_collection(driver, game)


def main():
    """
    Main function to update the BGG collection.
    """
    boardgames_data = read_boardgames_data(JSON_FILE_PATH)
    if boardgames_data is None:
        return

    driver = setup_driver()
    login_to_bgg(driver)
    update_bgg_collection(driver, boardgames_data)
    driver.quit()
    print("Script finished. Check your BoardGameGeek collection.")


if __name__ == "__main__":
    main()
