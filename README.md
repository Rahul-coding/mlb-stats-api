# MLB stats client
A lightweight user friendly client for fetching MLB stats data directly from the MLB API

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start & Methods](#quick-start--methods)
   - [get-pitcher-stats](#get-pitcher-stats)

# features
- **Flexible Identification**: Search for players stats using their name (`Shohei Ohtani`) or their MLB ID (`660271`). Search for team stats using their club name (`Yankees`), full name (`New York Yankees`), or abbreviation (`NYY`), all case insensitive.
- **Stats filtering**: Return only stats you want using the optional `fields` parameter to keep your outputs clean and concise.
- **Player statistics**: Return comprehensive player statistics for the current year, career, or even advanced metrics.
- **Team statistics**: Return team level hitting, pitching, or fielding metrics.

# Installation
Make sure you have the `requests` library installed:
```bash
pip install requests
```
Save the `mlb_stats_client` class into your project (e.g., mlb_client.py). This is not yet released to `pip`.

# Quick Start & Methods

## get-pitcher-stats
