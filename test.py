from mlb_stats import mlb_stats_client

client = mlb_stats_client()
data = client.get_stat_leaders(stat="homeRuns", season=2025, num_leaders=5, league="AL")
for player in data:
    print(f"{player["person"]['fullName']} - {player['value']} HRs")
