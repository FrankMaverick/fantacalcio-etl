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

# from utils import file_operations as file_ops
# from load.insert_player_name_mappings import insert_player_name_mappings
# from load.insert_sources import insert_source
# from load.insert_team_name_mappings import insert_team_name_mappings
# from load.truncate_tables import truncate_tables
# from logging_config import setup_logging
# from pathlib import Path
# from scrapers.fbr.team_season_stats import get_team_season_stats
# from scrapers.fbr.player_season_stats import get_player_season_stats
# from scrapers.football_api.players import players_to_dataframe
# from scrapers.football_api.players_teams import players_teams_to_dataframe
# from scrapers.football_api.teams import Teams, teams_to_dataframe
# from scrapers.football_api.api_client import fetch_players_data, fetch_players_teams_data, fetch_teams_data
#from load.create_tables import create_tables
#from load.drop_tables import drop_tables
# from load.insert_player_details import insert_player_details
# from load.insert_players import insert_players
# from load.insert_roles import insert_roles
# from load.insert_team_details import insert_team_details
# from load.insert_teams import insert_teams


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





    # # Extract players
    # if not Path(PLAYERS_FILE_JSON).is_file():
    #     logger.info(f"Extracting players for {FOOTAPI_SEASON} season")
    #     players_list = fetch_players_data(league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON)
    #     # Save players to json
    #     file_ops.save_json(players_list, PLAYERS_FILE_JSON)
    # else:
    #    logger.info(f"Players for {FOOTAPI_SEASON} season already extracted") 
    #    players_list = file_ops.read_json(PLAYERS_FILE_JSON)
    
    # players_df = players_to_dataframe(players_list)
    # players_df.to_csv('data/players_df.csv')
    
    # # Extract Teams
    # if not Path(TEAMS_FILE_JSON).is_file():
    #     logger.info(f"Extracting teams for {FOOTAPI_SEASON} season")
    #     teams_list = fetch_teams_data(league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON)
    #     # Save teams to json
    #     file_ops.save_json(teams_list, TEAMS_FILE_JSON)
    # else:
    #     logger.info(f"Teams for {FOOTAPI_SEASON} season already extracted") 
    #     teams_list = file_ops.read_json(TEAMS_FILE_JSON)
    
    # teams_df = teams_to_dataframe(teams_list)
    # #teams_df.to_csv('data/teams_df.csv')

    # # Extract Players for every Teams (not possible for historical data)
    # if not HISTORICAL_DATA:
    #     if not Path(PLAYERS_TEAMS_FILE_JSON).is_file():
    #         logger.info(f"Extracting players of teams for {FOOTAPI_SEASON} season")
    #         players_teams_list = fetch_players_teams_data(teams_list)
    #         # Save teams to json
    #         file_ops.save_json(players_teams_list, PLAYERS_TEAMS_FILE_JSON)
    #     else:
    #         logger.info(f"Players of teams for {FOOTAPI_SEASON} season already extracted") 
    #         players_teams_list = file_ops.read_json(PLAYERS_TEAMS_FILE_JSON)
    
    #     players_teams_df = players_teams_to_dataframe(players_teams_list)

    #     players_df = players_teams_df.merge(players_df, on='player_id', how='left')

    #     #players_df.to_csv('data/players_teams_df.csv')

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
