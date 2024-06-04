import soccerdata as sd
import pandas as pd


def get_team_season_stats(league, season):
    fbr = sd.FBref(leagues=league, seasons=season)
    return fbr.read_team_season_stats(stat_type="standard")
