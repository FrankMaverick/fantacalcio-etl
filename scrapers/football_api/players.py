from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player import Player
import logging

from models.player_details import PlayerDetails
from scrapers.football_api.api_client import fetch_players_data
from scrapers.football_api.utils import translate_nationality, translate_role, parse_date, transform_str_to_int

logger = logging.getLogger(__name__)

class Players:
    def __init__(self, db_path, historical_data=False):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.historical_data = historical_data

    def extract_data(self, league, season):
        """
        Estrae i dati dei giocatori dalla sorgente API.
        """
        return fetch_players_data(league, season)

    def map_data_to_dict(self, player_obj):
        """
        Trasforma i dati del giocatore in un dizionario
        """
        player = player_obj['player']
        role_principal = player_obj['statistics'][0]['games']['position'] if player_obj['statistics'] else None
        translated_role = translate_role(role_principal) if role_principal else None
        
        player_info = {
            'display_name': player['name'],
            'first_name': player['firstname'],
            'last_name': player['lastname'],
            'team_id': None,
            'role_principal': translated_role,
            'current_in_serie_a': None,
            'footballapi_id': player['id'],
            'height': transform_str_to_int(player['height']),
            'weight': transform_str_to_int(player['weight']),
            'birth_date':  parse_date(player['birth']['date']),
            'nationality': translate_nationality(player['nationality']),
            'img_url': player['photo']
        }
        return player_info

    def transform_data(self, players_data):
        """
        Mappa e Trasforma i dati dei giocatori
        """
        transformed_players = []
        for player_obj in players_data:
            transformed_player = self.map_data_to_dict(player_obj)
            transformed_players.append(transformed_player)
        return transformed_players 

    def save_data_to_db(self, players_data):
        session = self.Session()
        try:

            # Salva i player che non esistono già
            new_players = [player for player in players_data if not session.query(Player).filter_by(footballapi_id=player['footballapi_id']).first()]
            Player.save_players(session, new_players)

            # Salva i player_details
            player_details = [{
                'player_id': session.query(Player).filter_by(footballapi_id=player['footballapi_id']).first().id,
                'height': player['height'],
                'weight': player['weight'],
                'birth_date': player['birth_date'],
                'nationality': player['nationality'],
                'img_url': player['img_url']
            } for player in new_players]
            PlayerDetails.save_player_details(session, player_details)

            logger.info("Players saved to the database successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {e}")
        finally:
            session.close()


# def get_player_info(player_obj):
#     player = player_obj['player']
#     for stat in player_obj['statistics']:
#         player_info = {
#             'player_id': player['id'],
#             'player_name': player['name'],
#             'player_firstname': player['firstname'],
#             'player_lastname': player['lastname'],
#             'player_age': player['age'],
#             'player_birth_date': player['birth']['date'],
#             'player_birth_place': player['birth']['place'],
#             'player_birth_country': player['birth']['country'],
#             'player_nationality': player['nationality'],
#             'player_height': player['height'],
#             'player_weight': player['weight'],
#             'player_injured': player['injured'],
#             'player_photo': player['photo'],
#             # 'team_id': stat['team']['id'],
#             # 'team_name': stat['team']['name'],
#             # 'team_logo': stat['team']['logo'],
#             # 'league_id': stat['league']['id'],
#             # 'league_name': stat['league']['name'],
#             # 'league_country': stat['league']['country'],
#             # 'league_logo': stat['league']['logo'],
#             # 'league_flag': stat['league']['flag'],
#             # 'season': stat['league']['season'],
#             # 'games_appearences': stat['games']['appearences'],
#             # 'games_lineups': stat['games']['lineups'],
#             # 'games_minutes': stat['games']['minutes'],
#             # 'games_number': stat['games']['number'],
#             'games_position': stat['games']['position'],
#             # 'games_rating': stat['games']['rating'],
#             # 'games_captain': stat['games']['captain'],
#             # 'substitutes_in': stat['substitutes']['in'],
#             # 'substitutes_out': stat['substitutes']['out'],
#             # 'substitutes_bench': stat['substitutes']['bench'],
#             # 'shots_total': stat['shots']['total'],
#             # 'shots_on': stat['shots']['on'],
#             # 'goals_total': stat['goals']['total'],
#             # 'goals_conceded': stat['goals']['conceded'],
#             # 'goals_assists': stat['goals']['assists'],
#             # 'goals_saves': stat['goals']['saves'],
#             # 'passes_total': stat['passes']['total'],
#             # 'passes_key': stat['passes']['key'],
#             # 'passes_accuracy': stat['passes']['accuracy'],
#             # 'tackles_total': stat['tackles']['total'],
#             # 'tackles_blocks': stat['tackles']['blocks'],
#             # 'tackles_interceptions': stat['tackles']['interceptions'],
#             # 'duels_total': stat['duels']['total'],
#             # 'duels_won': stat['duels']['won'],
#             # 'dribbles_attempts': stat['dribbles']['attempts'],
#             # 'dribbles_success': stat['dribbles']['success'],
#             # 'dribbles_past': stat['dribbles']['past'],
#             # 'fouls_drawn': stat['fouls']['drawn'],
#             # 'fouls_committed': stat['fouls']['committed'],
#             # 'cards_yellow': stat['cards']['yellow'],
#             # 'cards_yellowred': stat['cards']['yellowred'],
#             # 'cards_red': stat['cards']['red'],
#             # 'penalty_won': stat['penalty']['won'],
#             # 'penalty_commited': stat['penalty']['commited'],
#             # 'penalty_scored': stat['penalty']['scored'],
#             # 'penalty_missed': stat['penalty']['missed'],
#             # 'penalty_saved': stat['penalty']['saved']
#         }
#     return player_info
