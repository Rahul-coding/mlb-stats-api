# MLB stats client
A lightweight user friendly client for fetching MLB stats data directly from the MLB API. Requires python version 3.x

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
   * [get-hitter-stats](#get-hitter-stats)
   * [get-pitcher-stats](#get-pitcher-stats)
   * [get-stat-leaders](#get-stat-leaders)
   * [get-team-stats](#get-team-stats)
   
5. [API Reference](#api-reference)
6. [Valid Parameter options](#valid-parameter-options)

# Features
* **Flexible Identification**: Search for players stats using their name (`Shohei Ohtani`) or their MLB ID (`660271`). Search for team stats using their club name (`Yankees`), full name (`New York Yankees`), or abbreviation (`NYY`), all case insensitive.
* **Stats filtering**: Return only stats you want using the optional `fields` parameter to keep your outputs clean and concise.
* **Player statistics**: Return comprehensive player statistics for the current year, career, or even advanced metrics.
* **Team statistics**: Return team level hitting, pitching, or fielding metrics.

# Installation
Make sure you have the `requests` library installed:
```bash
pip install requests
```
Save the `mlb_stats_client` class into your project (e.g., mlb_stats.py). This is not yet released to `pip`.

# Quick Start

## get-hitter-stats()
```
from mlb_stats import mlb_stats_client

client = mlb_stats_client()
print(client.get_hitter_stats("Mike Trout", stat_type="career", fields = ["avg", "homeRuns"])) #pull Mike Trout's carrer batting average and home runs
```

## get-pitcher-stats()
```
from mlb_stats import mlb_stats_client #import the library

client = mlb_stats_client() #set up the client
print(client.get_pitcher_stats("Jacob deGrom", stat_type="sabermetrics", fields = ["xfip", "war"])) #pull xfip and war from advanced metrics for Jacob DeGrom
```
## get_stat_leaders()
```
from mlb_stats import mlb_stats_client #import the library

client = mlb_stats_client()
data = client.get_stat_leaders(stat="homeRuns", season=2025, num_leaders=5, league="AL") #pull top 5 HR leaders for the AL

#output each player followed by their hrs (eg., Yordan Alvarez - 35)
for player in data: 
    print(f"{player["person"]['fullName']} - {player['value']} HRs")
```

## get-team-stats()
```
from mlb_stats import mlb_stats_client

client = mlb_stats_client()
print(client.get_team_stats("NYY", group = ["fielding"], fields = ["errors", "fielding"])) #get the Yankees errors and fielding% this year
```

# [API Reference](https://rahul-coding.github.io/mlb-stats-api/api-refernce/)

# Valid Parameter Options
What inputs you can use for the different parameters such as fields, group, etc

## get-hitter-stats()

**Params** 
1. **player** (Union[str, int]) -- Required 
    * the `player` parameter can take in either a **players full name** (eg., `Shohei Ohtani`) OR the **players id** (eg., `660271`).  
3. **fields** (list[str]) -- default `None` (all fields will be returned)
> Note arguments in the "advanced" category are only valid with the `sabermetrics` argument for `stat_type`

| Category    | Options  |
| --------    | -------- | 
| Basic/counts| gamesPlayed, plateAppearances, atBats, runs, hits, doubles, triples, homeRuns, totalBases, rbi, baseOnBalls, intentionalWalks, hitByPitch, strikeOuts, leftOnBase, numberOfPitches, age| 
| Slashes     | avg, obp, slg, ops, babip, atBatsPerHomeRun|
| Baserunning | stolenBases, caughtStealing, stolenBasePercentage, caughtStealingPercentage|
| Batted Ball | groundOuts, airOuts, groundOutsToAirouts, groundIntoDoublePlay, sacBunts, sacFlies, catchersInterference|
| Advanced    | woba, wRaa, wRc, wRcPlus, far, war, batting, fielding, baseRunning, positional, wLeague, replacement, spd, ubr, wGdp, wSb|



