from mlb_stats import mlb_stats_client

client = mlb_stats_client()
print(client.get_team_stats("Yankees", group = ["pitching", "hitting"], fields = ["wins", "losses", "era", "avg", "hr", "rbi"]))
