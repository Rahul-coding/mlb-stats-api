import requests
from typing import Union

class mlb_stats_client:
    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def get_player_id(self, name: str) -> int:
        #earch for a player by full name and return their MLB person_id.
        endpoint = f"{self.BASE_URL}/people/search?names={name}"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        people = data.get("people", [])
        
        if not people:
            raise ValueError(f"No player found matching name: '{name}'")
        
        return people[0]["id"]

    def convert_to_id(self, player_identifier: Union[str, int]) -> int:
        #Helper to ensure we have an integer ID, looking up names if needed.
        if isinstance(player_identifier, str):
            return self.get_player_id(player_identifier)
        return player_identifier

    def convert_team_to_id(self, team_identifier: Union[str, int]) -> int:
       #Helper to ensure we have an integer team ID
        if isinstance(team_identifier, str):
            return self.get_team_id(team_identifier)
        return team_identifier

    def get_pitcher_stats(self, player: Union[str, int], fields: list[str]):
        #Fetch current season pitching stats by player name or MLB ID.

        person_id = self.convert_to_id(player)
        endpoint = f"{self.BASE_URL}/people/{person_id}?hydrate=stats(group=[pitching],type=[season])"
        
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        try:
            stats = data["people"][0]["stats"][0]["splits"][0]["stat"]
            #check if specific fields were requested and filter the stats accordingly
            if fields:
                stats = {field: stats.get(field) for field in fields}
            return stats
        except (IndexError, KeyError):
            print(f"No pitching stats found for player: '{player}'")
            return {}

    def get_hitter_stats(self, player: Union[str, int], fields: list[str] = None):
       #Fetch current season hitting stats by player name or MLB ID.
        person_id = self.convert_to_id(player)
        endpoint = f"{self.BASE_URL}/people/{person_id}?hydrate=stats(group=[hitting],type=[season])"
        
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        try:
            stats = data["people"][0]["stats"][0]["splits"][0]["stat"]
            #check if specific fields were requested and filter the stats accordingly
            if fields:
                stats = {field: stats.get(field) for field in fields}
            return stats
        except (IndexError, KeyError):
            print(f"No hitting stats found for player: '{player}'")
            return {}
        
    def get_team_id(self, name: str) -> int:
        #Search for a team by name (e.g., 'Yankees' or 'New York Yankees') and return its team_id.
        endpoint = f"{self.BASE_URL}/teams?sportId=1"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        teams = data.get("teams", [])
        # Search match against team name, location, or short name case-insensitively
        name_lower = name.lower()
        for team in teams:
            team.pop("springLeague", None)  # Remove springLeague if present
            if (name_lower == team.get("clubName", "").lower() or 
                name_lower == team.get("name", "").lower() or
                name_lower == team.get("abbreviation", "").lower()):
                return team["id"]
                
        raise ValueError(f"No team found matching name: '{name}'")
            
    def get_team_stats(self, team: Union[str, int], fields: list[str] = None, group: list[str] = ["hitting", "pitching"], stat_type: str = "season"):
        # Fetch current season team stats by team name or ID using the dedicated /teams/stats endpoint.
        team_id = self.convert_team_to_id(team)
        
        all_group_stats = {}
        
        # Use the dedicated /teams/stats endpoint with parameters for group and stat type
        for group_type in group:
            endpoint = f"{self.BASE_URL}/teams/{team_id}/stats"
            params = {
                "teamId": team_id,
                "stats": stat_type,
                "group": group_type, 
                "season": 2026      
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()

            try:
                stats = data["stats"][0]["splits"][0]["stat"]
                
                # Filter fields if specified
                if fields:
                    stats = {field: stats.get(field) for field in fields if field in stats}
                    
                # Store stats under their respective group type
                all_group_stats[group_type] = stats
                
            except (IndexError, KeyError):
                print(f"No team stats found for team: '{team}' in group: '{group_type}'")
                continue #countinue to next group if one fails
                
        return all_group_stats