from config import FOOTAPI_LEAGUE, FOOTAPI_SEASON, FBR_LEAGUE, FBR_SEASON, PLAYERS_FILE_JSON, TEAMS_FILE_JSON, PLAYERS_TEAMS_FILE_JSON, HISTORICAL_DATA, FBR_SOURCE_NAME, DB_PATH
import logging
import pandas as pd 
from scrapers.football_api.players import Players
from scrapers.football_api.players_teams import PlayersTeams
from scrapers.football_api.teams import Teams
from models.database_utils import create_tables, drop_tables

from logging_config import setup_logging
from pathlib import Path

from utils.file_operations import load_from_file, save_to_file

# from load.insert_player_name_mappings import insert_player_name_mappings
# from load.insert_sources import insert_source
# from load.insert_team_name_mappings import insert_team_name_mappings
# from load.truncate_tables import truncate_tables
# from scrapers.fbr.team_season_stats import get_team_season_stats
# from scrapers.fbr.player_season_stats import get_player_season_stats
# from load.insert_player_details import insert_player_details
# from load.insert_players import insert_players

# Imposta il logging
setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Start")

    # Create tables
    #drop_tables()
    #create_tables()

    # Creare un'istanza di Teams
    teams = Teams(DB_PATH, HISTORICAL_DATA)

    if not Path(TEAMS_FILE_JSON).is_file():
        # Estrai i dati delle squadre
        teams_data = teams.extract_data(league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON)
        save_to_file(teams_data, TEAMS_FILE_JSON)

    teams_data = load_from_file(TEAMS_FILE_JSON)

    # Trasforma i dati delle squadre
    transformed_teams = teams.transform_data(teams_data)

    # Salva i dati delle squadre nel database
    teams.save_data_to_db(transformed_teams)

    # Creare un'istanza di Players
    players = Players(DB_PATH, HISTORICAL_DATA)

    if not Path(PLAYERS_FILE_JSON).is_file():
        # Estrai i dati dei giocatori
        players_data = players.extract_data(league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON)
        save_to_file(players_data, PLAYERS_FILE_JSON)

    players_data = load_from_file(PLAYERS_FILE_JSON)

    # Trasforma i dati delle squadre
    transformed_players = players.transform_data(players_data)

    # Salva i dati dei giocatori nel database
    players.save_data_to_db(transformed_players)


    # Creare un'istanza di PlayersTeams
    players_teams = PlayersTeams(DB_PATH, HISTORICAL_DATA)
    if not Path(PLAYERS_TEAMS_FILE_JSON).is_file():
        players_teams_data = players_teams.extract_data()
        save_to_file(players_teams_data, PLAYERS_TEAMS_FILE_JSON)

    players_teams_data = load_from_file(PLAYERS_TEAMS_FILE_JSON)

    # Trasforma i dati dei giocatori delle squadre
    transformed_players_teams = players_teams.transform_data(players_teams_data)

    # Salve i dati players_teams a db
    players_teams.save_data_to_db(transformed_players_teams)


    

    # #forse qui non cambia niente se sono dati storici o meno ?
    # # team_season_stats_df  = get_team_season_stats(FBR_LEAGUE, FBR_SEASON)
    # # team_season_stats_df.reset_index(inplace=True)
    # # team_season_stats_df.to_csv(f'data/team_season_stats_df_{FBR_SEASON}.csv', encoding="utf-8")
    # team_season_stats_df = pd.read_csv(f'data/team_season_stats_df_{FBR_SEASON}.csv')
    # fbr_teams = team_season_stats_df[['team']].dropna(axis='rows').copy()

    # #forse qui non cambia niente se sono dati storici o meno ?
    # # player_season_stats_df  = get_player_season_stats(FBR_LEAGUE, FBR_SEASON)
    # # player_season_stats_df.reset_index(inplace=True)
    # # player_season_stats_df.to_csv(f'data/player_season_stats_df_{FBR_SEASON}.csv', encoding="utf-8")
    # player_season_stats_df = pd.read_csv(f'data/player_season_stats_df_{FBR_SEASON}.csv')
    # fbr_players_teams = player_season_stats_df[['team','player']].dropna(axis='rows').copy()    

    # # Insert data
    # # teams
    # insert_teams(teams_df, HISTORICAL_DATA)
    # insert_team_details(teams_df)

    # # players
    # insert_players(players_df, HISTORICAL_DATA)
    # insert_player_details(players_df)

    # # roles
    # insert_roles(players_df, HISTORICAL_DATA)

    # # ## FBREF DATA
    # # insert_source(FBR_SOURCE_NAME)
    # # # Team mappings from FBRef
    # # insert_team_name_mappings(fbr_teams[['team']], FBR_SOURCE_NAME)
    # # insert_player_name_mappings(fbr_players_teams[['team','player']], FBR_SOURCE_NAME)
