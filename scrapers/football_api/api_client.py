import requests
from config import API_KEY
import logging
import time

logger = logging.getLogger(__name__)

def call_api(endpoint, params=None):
    url = f'https://v3.football.api-sports.io/{endpoint}'
    headers = {
        'x-rapidapi-key': API_KEY 
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # Stampa gli header di rate limiting
        rate_limit_headers = {
            #'x-ratelimit-requests-limit': response.headers.get('x-ratelimit-requests-limit'),
            'x-ratelimit-requests-remaining': response.headers.get('x-ratelimit-requests-remaining'),
            #'X-RateLimit-Limit': response.headers.get('X-RateLimit-Limit'),
            'X-RateLimit-Remaining': response.headers.get('X-RateLimit-Remaining')
        }
        for key, value in rate_limit_headers.items():
            logger.debug(f'{key}: {value}')
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'An error occurred: {e}')
        return None

# funzione ricorsiva per ottenere i dati dei giocatori
def fetch_players_data(league, season, page=1, players_data=[]):
    params = {
        'league': league,
        'season': season,
        'page': page
    }
    players = call_api('players', params)
    players_data.extend(players['response'])

    if players['paging']['current'] < players['paging']['total']:
        logger.debug(f"Page {players['paging']['current']} of {players['paging']['total']}")
        page += 1
        time.sleep(6.1)  # Pausa di 6 sec per evitare di superare il rate limit (10 req / min)
        return fetch_players_data(league, season, page, players_data)
    
    return players_data

# funzione per estrarre i dati dei teams
def fetch_teams_data(league, season):
    teams_data = []
    params = {
        'league': league,
        'season': season,
    }
    teams = call_api('teams', params)
    teams_data.extend(teams['response'])
    
    return teams_data

# funzione per estrarre i player di un team
def fetch_players_teams_data(team_ids):
    players_teams_data = []
    for team_id in team_ids:
        logger.debug(f"Extracting players of team: {team_id}")
        players_team_data = fetch_players_team_data(team_id)
        players_teams_data.extend(players_team_data)
        time.sleep(6.1)  # Pausa di 6 sec per evitare di superare il rate limit (10 req / min)
    return players_teams_data
    

# funzione per estrarre i player di un team
def fetch_players_team_data(team_id):
    players_team_data = []
    params = {
        'team': team_id,
    }
    players = call_api('players/squads', params)
    players_team_data.extend(players['response'])
    
    return players_team_data
