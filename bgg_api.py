import requests
import xml.etree.ElementTree as ET
import time

def get_bgg_game_details(game_title):
    """
    Searches for a board game on BoardGameGeek and returns its details.
    It searches for the game by title, finds the most popular version (by rank),
    and returns its BGG URL, rank, average score, and other stats.
    """
    search_url = f"https://boardgamegeek.com/xmlapi2/search?query={game_title}&type=boardgame"
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        root = ET.fromstring(search_response.content)

        items = root.findall(".//item")
        if not items:
            return None

        game_ids = [item.get("id") for item in items if item.get("id")]
        if not game_ids:
            return None

        all_game_candidates = []
        for i in range(0, len(game_ids), 20):
            chunk = game_ids[i:i + 20]
            thing_url = f"https://boardgamegeek.com/xmlapi2/thing?id={','.join(chunk)}&stats=1"
            thing_response = requests.get(thing_url)
            thing_response.raise_for_status()
            thing_root = ET.fromstring(thing_response.content)

            for item in thing_root.findall(".//item"):
                game_id = item.get("id")
                rank_value = float('inf')
                score_value = 0.0

                rank_element = item.find(".//rank[@name='boardgame']")
                if rank_element is not None and rank_element.get("value") != "Not Ranked":
                    try:
                        rank_value = int(rank_element.get("value"))
                    except (ValueError, TypeError):
                        pass

                score_element = item.find(".//average")
                if score_element is not None:
                    try:
                        score_value = float(score_element.get("value"))
                    except (ValueError, TypeError):
                        pass

                min_players_element = item.find(".//minplayers")
                min_players = int(min_players_element.get("value")) if min_players_element is not None and min_players_element.get("value") else 0
                max_players_element = item.find(".//maxplayers")
                max_players = int(max_players_element.get("value")) if max_players_element is not None and max_players_element.get("value") else 0

                min_playtime_element = item.find(".//minplaytime")
                min_playtime = int(min_playtime_element.get("value")) if min_playtime_element is not None and min_playtime_element.get("value") else 0
                max_playtime_element = item.find(".//maxplaytime")
                max_playtime = int(max_playtime_element.get("value")) if max_playtime_element is not None and max_playtime_element.get("value") else 0

                weight_element = item.find(".//averageweight")
                weight = float(weight_element.get("value")) if weight_element is not None and weight_element.get("value") else 0.0

                all_game_candidates.append({
                    'id': game_id, 'rank': rank_value, 'score': score_value,
                    'min_players': min_players, 'max_players': max_players,
                    'min_playtime': min_playtime, 'max_playtime': max_playtime,
                    'weight': weight
                })

            if len(game_ids) > 20:
                time.sleep(1)

        if not all_game_candidates:
            return None

        all_game_candidates.sort(key=lambda x: x['rank'])
        best_game = all_game_candidates[0]

        return {
            "url": f"https://boardgamegeek.com/boardgame/{best_game['id']}",
            "rank": best_game['rank'] if best_game['rank'] != float('inf') else "Not Ranked",
            "score": round(best_game['score'], 2),
            "min_players": best_game['min_players'],
            "max_players": best_game['max_players'],
            "min_playtime": best_game['min_playtime'],
            "max_playtime": best_game['max_playtime'],
            "weight": round(best_game['weight'], 2)
        }

    except requests.exceptions.RequestException as e:
        print(f"Error querying BGG API for '{game_title}': {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML for '{game_title}': {e}")
    return None
