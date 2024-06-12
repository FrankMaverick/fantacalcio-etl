from config import FOOTAPI_LEAGUE, FOOTAPI_SEASON, FBR_LEAGUE, FBR_SEASON, PLAYERS_FILE_JSON, TEAMS_FILE_JSON, PLAYERS_TEAMS_FILE_JSON, HISTORICAL_DATA, FBR_SOURCE_NAME, DB_PATH
import logging
import pandas as pd 
from scrapers.fbr.scraper_fbr import ScraperFBR
from scrapers.football_api.players import Players as FootballAPIPlayers
from scrapers.football_api.players_teams import PlayersTeams as FootballAPIPlayersTeams
from scrapers.football_api.teams import Teams as FootballAPITeams
from scrapers.fbr.teams import Teams as FBRTeams
from scrapers.fbr.players import Players as FBRPlayers
from models.database_utils import create_tables, drop_tables
from utils.file_operations import load_from_file, save_to_file
from pathlib import Path
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Start")

    # Create tables
    #drop_tables()
    #create_tables()

    # Creare un'istanza di Teams
    teams = FootballAPITeams(DB_PATH, league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON, historical_data=HISTORICAL_DATA)

    if not Path(TEAMS_FILE_JSON).is_file():
        # Estrai i dati delle squadre
        teams_data = teams.extract_data()
        save_to_file(teams_data, TEAMS_FILE_JSON)

    teams_data = load_from_file(TEAMS_FILE_JSON)

    # Trasforma i dati delle squadre
    transformed_teams = teams.transform_data(teams_data)

    # Salva i dati delle squadre nel database
    teams.save_data_to_db(transformed_teams)

    # Creare un'istanza di Players
    players = FootballAPIPlayers(DB_PATH, league=FOOTAPI_LEAGUE, season=FOOTAPI_SEASON, historical_data=HISTORICAL_DATA)

    if not Path(PLAYERS_FILE_JSON).is_file():
        # Estrai i dati dei giocatori
        players_data = players.extract_data()
        save_to_file(players_data, PLAYERS_FILE_JSON)

    players_data = load_from_file(PLAYERS_FILE_JSON)

    # Trasforma i dati delle squadre
    transformed_players = players.transform_data(players_data)

    # Salva i dati dei giocatori nel database
    players.save_data_to_db(transformed_players)


    # Creare un'istanza di PlayersTeams
    players_teams = FootballAPIPlayersTeams(DB_PATH, HISTORICAL_DATA)
    if not Path(PLAYERS_TEAMS_FILE_JSON).is_file():
        players_teams_data = players_teams.extract_data()
        save_to_file(players_teams_data, PLAYERS_TEAMS_FILE_JSON)

    players_teams_data = load_from_file(PLAYERS_TEAMS_FILE_JSON)

    # Trasforma i dati dei giocatori delle squadre
    transformed_players_teams = players_teams.transform_data(players_teams_data)

    # Salve i dati players_teams a db
    players_teams.save_data_to_db(transformed_players_teams)


    ### FBRef
    scraper_fbr = ScraperFBR(DB_PATH)
    scraper_fbr.add_source(source_name=FBR_SOURCE_NAME)
    #Teams
    teams_fbr = FBRTeams(DB_PATH, FBR_SOURCE_NAME, FBR_LEAGUE, FBR_SEASON, HISTORICAL_DATA)
    teams_fbr_data = teams_fbr.extract_data()
    transformed_teams_fbr = teams_fbr.transform_data(teams_fbr_data)
    teams_fbr.save_data_to_db(transformed_teams_fbr)
    #Players
    players_fbr = FBRPlayers(DB_PATH, FBR_SOURCE_NAME, FBR_LEAGUE, FBR_SEASON, HISTORICAL_DATA)
    players_fbr_data = players_fbr.extract_data()
    transformed_players_fbr = players_fbr.transform_data(players_fbr_data)
    #print(transformed_players_fbr)
    players_fbr.save_data_to_db(transformed_players_fbr)

