from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.team import Team 
from models.player import Player 
from scrapers.football_api.api_client import fetch_players_teams_data

import logging

from scrapers.football_api.utils import translate_role
logger = logging.getLogger(__name__)

class PlayersTeams:
    def __init__(self, db_path, historical_data=False):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.historical_data = historical_data

    def get_serie_a_team_footballapi_ids(self):
        """
        Estrae gli ID di football_api dei team di Serie A dal database
        """
        if self.historical_data:
            logger.info("Historical data mode enabled, skipping Serie A team extraction.")
            return []
    
        session = self.Session()
        try:
            serie_a_teams = session.query(Team).filter_by(current_in_serie_a=True).all()
            serie_a_team_ids = [team.footballapi_id for team in serie_a_teams]
            return serie_a_team_ids
        finally:
            session.close()        

    def extract_data(self):
        """
        Estrae i dati dei giocatori per i team di Serie A
        """
        if self.historical_data:
            logger.info("Historical data mode enabled, skipping data extraction.")
            return []        
        serie_a_team_ids = self.get_serie_a_team_footballapi_ids()
        return fetch_players_teams_data(serie_a_team_ids)
    
    def map_data_to_dict(self, player_team_obj):
        """
        Trasforma i dati dei giocatori di un team in un dizionario
        """
        team_id = player_team_obj['team']['id']
        players_data = []

        for player in player_team_obj['players']:
            role_principal = player['position'] if player['position'] else None
            translated_role = translate_role(role_principal) if role_principal else None
            player_data = {
                'footballapi_player_id': player['id'],
                'player_number': player['number'],
                'role_principal': translated_role,
                'footballapi_team_id': team_id,
                #'team_name': team_name,
            }
            players_data.append(player_data)

        return players_data

    def transform_data(self, players_teams_data):
        """
        Mappa e Trasforma i dati dei giocatori del team
        """
        if self.historical_data:
            logger.info("Historical data mode enabled, skipping data transformation.")
            return []
                
        transformed_players = []

        for player_team_obj in players_teams_data:
            players_data = self.map_data_to_dict(player_team_obj)
            transformed_players.extend(players_data)

        return transformed_players
    
    def save_data_to_db(self, players_teams_data):
        """
        Scrive i dati dei giocatori del team nel database
        """
        if self.historical_data:
            logger.info("Historical data mode enabled, skipping database write operations.")
            return

        session = self.Session()

        try:
            Player.set_all_current_in_serie_a_false(session)
            Player.set_all_team_id_null(session)

            for player_team_obj in players_teams_data:
                footballapi_player_id = player_team_obj['footballapi_player_id']
                footballapi_team_id = player_team_obj['footballapi_team_id']

                # Ricava il giocatore dal footballapi_player_id
                player = Player.get_player_by_footballapi_id(session, footballapi_player_id)

                # Ricava il team dal footballapi_team_id
                team = Team.get_team_by_footballapi_id(session, footballapi_team_id)

                if player:
                    # Aggiorna il giocatore impostando current_in_serie_a = True e team_id
                    player.current_in_serie_a = True
                    player.team_id = team.id

            session.commit()
            logger.info("Players teams data written to the database successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {e}")
        finally:
            session.close()    