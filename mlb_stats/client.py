from __future__ import annotations
from typing import Union
import requests

class mlb_stats_client:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def get_player_id(self, name: str) -> int:
        """Search for a player by full name and return their MLB person_id.

        Args:
            name: The full name of the player to search for.

        Returns:
            The MLB person_id of the player.

        Raises:
            ValueError: If no player is found with the given name.
        """
        endpoint = f"{self.BASE_URL}/people/search?names={name}"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        people = data.get("people", [])
        
        if not people:
            raise ValueError(f"No player found matching name: '{name}'")
        
        return people[0]["id"]

    def convert_to_id(self, player_identifier: Union[str, int]) -> int:
        """Helper to ensure we have an integer ID, looking up names if needed.

        Args:
            player_identifier: The player's name or ID.

        Returns:
            The MLB person_id of the player.

        Raises:
            ValueError: If no player is found with the given name.
        """
        if isinstance(player_identifier, str):
            return self.get_player_id(player_identifier)
        return player_identifier

    def convert_team_to_id(self, team_identifier: Union[str, int]) -> int:
        """Helper to ensure we have an integer team ID.

        Args:
            team_identifier: The team's name or ID.

        Returns:
            The MLB team_id of the team.

        Raises:
            ValueError: If no team is found with the given name.
        """
        if isinstance(team_identifier, str):
            return self.get_team_id(team_identifier)
        return team_identifier

    def get_pitcher_stats(self, player: Union[str, int], fields: list[str] = None, stat_type: str = "season", season: int = 2026) -> dict:
        """Fetch current season pitching stats by player name or MLB ID.

        Args:
            player: The player's name or MLB ID.
            fields: Specific stat fields to return. Defaults to None (return all).
            stat_type: Type of stats to fetch (e.g., "season", "career"). Defaults to "season".
            season: The season year for which to fetch stats. Defaults to 2026.

        Returns:
            A dictionary containing the requested pitching stats.

        Raises:
            ValueError: If no player is found with the given name.
        """
        person_id = self.convert_to_id(player)
        endpoint = f"{self.BASE_URL}/people/{person_id}?hydrate=stats(group=[pitching],type=[{stat_type}],season={season})"
        
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        try:
            stats = data["people"][0]["stats"][0]["splits"][0]["stat"]
            if fields:
                stats = {field: stats.get(field) for field in fields}
            return stats
        except (IndexError, KeyError):
            print(f"No pitching stats found for player: '{player}'")
            return {}

    def get_hitter_stats(self, player: Union[str, int], fields: list[str] = None, stat_type: str = "season", season: int = 2026) -> dict:
        """Fetch current season hitting stats by player name or MLB ID.

        Args:
            player: The player's name or MLB ID.
            fields: Specific stat fields to return. Defaults to None (return all).
            stat_type: Type of stats to fetch (e.g., "season", "career"). Defaults to "season".

        Returns:
            A dictionary containing the requested hitting stats.

        Raises:
            ValueError: If no player is found with the given name.
            season: The season year for which to fetch stats. Defaults to 2026.
        """
        person_id = self.convert_to_id(player)
        endpoint = endpoint = f"{self.BASE_URL}/people/{person_id}?hydrate=stats(group=[hitting],type=[{stat_type}],season={season})"
        
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        try:
            stats = data["people"][0]["stats"][0]["splits"][0]["stat"]
            if fields:
                stats = {field: stats.get(field) for field in fields}
            return stats
        except (IndexError, KeyError):
            print(f"No hitting stats found for player: '{player}'")
            return {}
        
    def get_team_id(self, name: str) -> int:
        """Search for a team by name (e.g., 'Yankees' or 'New York Yankees') and return its team_id.

        Args:
            name: The name of the team to search for.

        Returns:
            The MLB team_id of the team.

        Raises:
            ValueError: If no team is found with the given name.
        """
        endpoint = f"{self.BASE_URL}/teams?sportId=1"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        teams = data.get("teams", [])
        name_lower = name.lower()
        for team in teams:
            team.pop("springLeague", None)
            if (name_lower == team.get("clubName", "").lower() or 
                name_lower == team.get("name", "").lower() or
                name_lower == team.get("abbreviation", "").lower()):
                return team["id"]
                
        raise ValueError(f"No team found matching name: '{name}'")
            
    def get_team_stats(self, team: Union[str, int], fields: list[str] = None, group: list[str] = ["hitting", "pitching"]) -> dict:
        """Fetch current season team stats by team name or ID using the dedicated /teams/stats endpoint.

        Args:
            team: The team's name or MLB ID.
            fields: Specific stat fields to return. Defaults to None (return all).
            group: List of stat groups to fetch (e.g., ["hitting", "pitching"]). Defaults to both.

        Returns:
            A dictionary containing the requested team stats, organized by group type.

        Raises:
            ValueError: If no team is found with the given name.
        """
        team_id = self.convert_team_to_id(team)
        all_group_stats = {}
        
        for group_type in group:
            endpoint = f"{self.BASE_URL}/teams/{team_id}/stats"
            params = {
                "teamId": team_id,
                "stats": "season",
                "group": group_type, 
                "season": 2026      
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()

            try:
                stats = data["stats"][0]["splits"][0]["stat"]
                if fields:
                    stats = {field: stats.get(field) for field in fields if field in stats}
                all_group_stats[group_type] = stats
            except (IndexError, KeyError):
                print(f"No team stats found for team: '{team}' in group: '{group_type}'")
                continue
                
        return all_group_stats
    def get_stat_leaders(self, stat: str, group: str = "hitting", season: int = 2026, num_leaders: int = 10, league: str = "") -> list[dict]:
        """Fetch the top players in a specific stat category for the current season.

        Args:
            stat: The stat category to fetch leaders for (e.g., "homeRuns", "strikeOuts").
            group: The stat group to fetch from ("hitting" or "pitching"). Defaults to "hitting".
            season: The season year for which to fetch leaders. Defaults to 2026.
            num_leaders: The maximum number of leaders to return. Defaults to 10.
            league: The league for which to fetch leaders. Defaults to "" (all leagues).

        Returns:
            A list of dictionaries containing the top players and their stats in the specified category.
        """
        endpoint = f"{self.BASE_URL}/stats/leaders"
        params = {
            "statGroup": group,
            "statType": "season",
            "season": season,
            "limit": num_leaders,
            "leaderCategories": stat
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        data = response.json()
        try:
            leaders = data["leagueLeaders"][0]["leaders"]
            if(league):
                leaders = [leader for leader in leaders if leader.get("league", {}).get("name", "").lower() == league.lower()]
            return leaders
        except (IndexError, KeyError):
            print(f"No leaders found for stat: '{stat}' in group: '{group}' for season: {season}")
            return []