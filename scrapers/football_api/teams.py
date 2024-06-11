from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapers.football_api.api_client import fetch_teams_data
from models.team import Team
from models.team_details import TeamDetails
import logging

logger = logging.getLogger(__name__)

class Teams:
    def __init__(self, db_path, historical_data=False):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.historical_data = historical_data

    def extract_data(self, league, season):
        """
        Estrae i dati delle squadre dalla sorgente API.
        """
        return fetch_teams_data(league, season)
    
    def map_data_to_dict(self, team_obj):
        """
        Trasforma i dati del team in un dizionario
        """
        team_data = {
            'footballapi_id': team_obj['team']['id'],
            'team_name': team_obj['team']['name'],
            'team_code': team_obj['team']['code'],
            'team_country': team_obj['team']['country'],
            'team_founded': team_obj['team']['founded'],
            'current_in_serie_a': True if not self.historical_data else None,
            # 'team_national': team_obj['team']['national'],
            'team_logo_url': team_obj['team']['logo'],
            #'venue_id': team_obj['venue']['id'],
            'stadium_name': team_obj['venue']['name'],
            #'venue_address': team_obj['venue']['address'],
            'stadium_city': team_obj['venue']['city'],
            'stadium_capacity': team_obj['venue']['capacity'],
            #'venue_surface': team_obj['venue']['surface'],
            'stadium_img_url': team_obj['venue']['image']
        }
        return team_data       

    def transform_data(self, teams_data):
        """
        Mappa e Trasforma i dati delle squadre
        """
        transformed_teams = []
        for team_obj in teams_data:
            transformed_team = self.map_data_to_dict(team_obj)
            transformed_teams.append(transformed_team)
        return transformed_teams 

    def save_data_to_db(self, teams_data):
        session = self.Session()
        try:
            if not self.historical_data:
                Team.set_all_current_in_serie_a_false(session)

            # Salva i team che non esistono già
            new_teams = [team for team in teams_data if not session.query(Team).filter_by(footballapi_id=team['footballapi_id']).first()]
            Team.save_teams(session, new_teams)

            # Salva i team_details
            team_details = [{
                'team_id': session.query(Team).filter_by(footballapi_id=team['footballapi_id']).first().id,
                'stadium_name': team['stadium_name'],
                'stadium_city': team['stadium_city'],
                'stadium_capacity': team['stadium_capacity'],
                'stadium_img_url': team['stadium_img_url']
            } for team in teams_data]
            TeamDetails.save_team_details(session, team_details)

            if not self.historical_data:
                team_footballapi_ids = [team['footballapi_id'] for team in teams_data]
                Team.update_current_in_serie_a(session, team_footballapi_ids, True)

            logger.info("Teams and team details saved to the database successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {e}")
        finally:
            session.close()