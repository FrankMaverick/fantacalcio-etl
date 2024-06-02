from dotenv import load_dotenv
import os

# Carica le variabili di ambiente dal file .env
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'db/fantacalcio.db')}"
API_KEY = os.getenv('API_KEY')

# Football API
LEAGUE = 135
SEASON = 2023

# Json Files
PLAYERS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/players_{SEASON}.json')}"
TEAMS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/teams_{SEASON}.json')}"
PLAYERS_TEAMS_FILE_JSON = f"{os.path.join(BASE_DIR, f'data/players_teams_{SEASON}.json')}"

# data
HISTORICAL_DATA = False