from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player import Player
import logging

from models.player_details import PlayerDetails
from scrapers.football_api.api_client import fetch_players_data
from scrapers.football_api.utils import translate_nationality, translate_role, parse_date, transform_str_to_int

logger = logging.getLogger(__name__)

class Players:
    def __init__(self, db_path, league, season, historical_data=False):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.historical_data = historical_data
        self.league = league
        self.season = season

    def extract_data(self):
        """
        Estrae i dati dei giocatori dalla sorgente API.
        """
        return fetch_players_data(self.league, self.season)

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