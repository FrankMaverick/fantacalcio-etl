from football_api.players import players_to_dataframe
from football_api.players_teams import players_teams_to_dataframe
from football_api.teams import teams_to_dataframe
from scripts.create_tables import create_tables
from football_api.call_api import fetch_players_data, fetch_players_teams_data, fetch_teams_data
from scripts.drop_tables import drop_tables
from scripts.insert_players import insert_players
from scripts.insert_team_details import insert_team_details
from scripts.insert_teams import insert_teams
from utils import file_operations as file_ops
from config import LEAGUE, SEASON, PLAYERS_FILE_JSON, TEAMS_FILE_JSON, PLAYERS_TEAMS_FILE_JSON, HISTORICAL_DATA
import logging
from logging_config import setup_logging
from pathlib import Path

# Imposta il logging
setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Start")

    # Create tables
    drop_tables()
    create_tables()
    
    # Extract players
    if not Path(PLAYERS_FILE_JSON).is_file():
        logger.info(f"Extracting players for {SEASON} season")
        players_list = fetch_players_data(league=LEAGUE, season=SEASON)
        # Save players to json
        file_ops.save_json(players_list, PLAYERS_FILE_JSON)
    else:
       logger.info(f"Players for {SEASON} season already extracted") 
       players_list = file_ops.read_json(PLAYERS_FILE_JSON)
    
    players_df = players_to_dataframe(players_list)
    #players_df.to_csv('data/players_df.csv')
    
    # Extract Teams
    if not Path(TEAMS_FILE_JSON).is_file():
        logger.info(f"Extracting teams for {SEASON} season")
        teams_list = fetch_teams_data(league=LEAGUE, season=SEASON)
        # Save teams to json
        file_ops.save_json(teams_list, TEAMS_FILE_JSON)
    else:
        logger.info(f"Teams for {SEASON} season already extracted") 
        teams_list = file_ops.read_json(TEAMS_FILE_JSON)
    
    teams_df = teams_to_dataframe(teams_list)
    #teams_df.to_csv('data/teams_df.csv')

    # Extract Players for every Teams (not possible for historical data)
    if not HISTORICAL_DATA:
        if not Path(PLAYERS_TEAMS_FILE_JSON).is_file():
            logger.info(f"Extracting players of teams for {SEASON} season")
            players_teams_list = fetch_players_teams_data(teams_list)
            # Save teams to json
            file_ops.save_json(players_teams_list, PLAYERS_TEAMS_FILE_JSON)
        else:
            logger.info(f"Players of teams for {SEASON} season already extracted") 
            players_teams_list = file_ops.read_json(PLAYERS_TEAMS_FILE_JSON)
    
        players_teams_df = players_teams_to_dataframe(players_teams_list)

        #players_teams_df.to_csv('data/players_teams_df.csv')

        players_df = players_teams_df.merge(players_df, on='player_id', how='left')

        #players_df.to_csv('data/players_teams_df.csv')


    # Insert data
    # teams
    insert_teams(teams_df, HISTORICAL_DATA)
    insert_team_details(teams_df)

    # next step
    insert_players(players_df, HISTORICAL_DATA)
