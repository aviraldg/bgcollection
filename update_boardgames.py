import json
import sys
import time

from bgg_api import get_bgg_game_details


def read_boardgames_data(json_file_path):
    """Reads board games data from a JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        return None


def write_boardgames_data(json_file_path, data):
    """Writes board games data to a JSON file."""
    try:
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"Error writing to file {json_file_path}: {e}")
        return False


def update_boardgames_data(boardgames_data):
    """
    Updates board games data with BGG URL, rank, score, and other stats.
    """
    updated_count = 0
    details_to_check = ["url", "rank", "score", "min_players", "max_players", "min_playtime", "max_playtime", "weight"]

    for game in boardgames_data:
        title = game.get("title")
        details_missing = not all(k in game for k in details_to_check) or not game.get("url")

        if title and details_missing:
            print(f"Fetching details for '{title}'...")
            max_retries = 3
            details = None
            for attempt in range(max_retries):
                details = get_bgg_game_details(title)
                if details:
                    game.update(details)
                    updated_count += 1
                    print(f"Updated details for '{title}': Rank {details['rank']}, Score {details['score']}, Weight {details['weight']}")
                    break
                else:
                    print(f"Could not find details for '{title}' (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(10)

            if not details:
                for key in details_to_check:
                    if key not in game:
                        game[key] = None if key == 'url' else "Not Found" if key == 'rank' else 0

            time.sleep(5)

    return updated_count, boardgames_data


def main(json_file_path):
    """
    Main function to update the board games JSON file.
    """
    boardgames_data = read_boardgames_data(json_file_path)
    if boardgames_data is None:
        return

    updated_count, updated_data = update_boardgames_data(boardgames_data)

    if updated_count > 0:
        if write_boardgames_data(json_file_path, updated_data):
            print(f"\nSuccessfully updated {updated_count} board games in {json_file_path}")
    else:
        print("\nAll board games are already up-to-date.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        main(json_file)
    else:
        print("Usage: python update_boardgames.py <path_to_json_file>")