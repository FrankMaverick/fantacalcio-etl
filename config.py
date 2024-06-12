from dotenv import load_dotenv
import os

# Carica le variabili di ambiente dal file .env
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'db/fantacalcio.db')}"
API_KEY = os.getenv('API_KEY')

# data
HISTORICAL_DATA = False
SEASON = 2023

# Football API Source
FOOTAPI_LEAGUE = 135
FOOTAPI_SEASON = SEASON

# FBR Source
FBR_SOURCE_NAME = 'FBR'
FBR_LEAGUE = 'ITA-Serie A'
FBR_SEASON = SEASON

# Json Files
PLAYERS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/players_{FOOTAPI_SEASON}.json')}"
TEAMS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/teams_{FOOTAPI_SEASON}.json')}"
PLAYERS_TEAMS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/players_teams_{FOOTAPI_SEASON}.json')}"
