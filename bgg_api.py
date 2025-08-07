import requests
import xml.etree.ElementTree as ET
import time


class BggApi:
    def __init__(self, api_url="https://boardgamegeek.com/xmlapi2"):
        self.api_url = api_url

    def _make_request(self, url, params=None):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
        except ET.ParseError as e:
            print(f"Error parsing XML from {url}: {e}")
        return None

    def search_game(self, title):
        search_url = f"{self.api_url}/search"
        params = {"query": title, "type": "boardgame"}
        root = self._make_request(search_url, params=params)
        if root is None:
            return []
        return [item.get("id") for item in root.findall(".//item") if item.get("id")]

    def get_game_details(self, game_ids):
        thing_url = f"{self.api_url}/thing"
        params = {"id": ",".join(game_ids), "stats": 1}
        root = self._make_request(thing_url, params=params)
        if root is None:
            return []

        games = []
        for item in root.findall(".//item"):
            games.append(self._parse_game_details(item))
        return games

    def _parse_game_details(self, item):
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

        return {
            'id': game_id, 'rank': rank_value, 'score': score_value,
            'min_players': min_players, 'max_players': max_players,
            'min_playtime': min_playtime, 'max_playtime': max_playtime,
            'weight': weight
        }

    def get_bgg_game_details(self, game_title):
        """
        Searches for a board game on BoardGameGeek and returns its details.
        It searches for the game by title, finds the most popular version (by rank),
        and returns its BGG URL, rank, average score, and other stats.
        """
        game_ids = self.search_game(game_title)
        if not game_ids:
            return None

        all_game_candidates = []
        for i in range(0, len(game_ids), 20):
            chunk = game_ids[i:i + 20]
            all_game_candidates.extend(self.get_game_details(chunk))
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
