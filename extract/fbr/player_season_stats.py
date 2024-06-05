import soccerdata as sd

def get_player_season_stats(league, season):
    fbr = sd.FBref(leagues=league, seasons=season)
    return fbr.read_player_season_stats(stat_type="standard")
