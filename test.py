from mlb_stats import mlb_stats_client

client = mlb_stats_client()
print(client.get_team_stats("NYY", group = ["fielding"], fields = ["errors", "fielding"]))
