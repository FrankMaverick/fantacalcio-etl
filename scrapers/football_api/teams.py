from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapers.football_api.api_client import fetch_teams_data
from models.team import Team
from models.team_details import TeamDetails
import logging

logger = logging.getLogger(__name__)

class Teams:
    def __init__(self, db_path, league, season, historical_data=False):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.historical_data = historical_data
        self.league = league
        self.season = season
        self._extracted_data = None
        self._transformed_data = None

    @property
    def extracted_data(self):
        return self._extracted_data

    @extracted_data.setter
    def extracted_data(self, data):
        self._extracted_data = data

    @property
    def transformed_data(self):
        return self._transformed_data

    @transformed_data.setter
    def transformed_data(self, data):
        self._transformed_data = data               

    def extract(self):
        """
        Estrae i dati delle squadre dalla sorgente API.
        """
        self._extracted_data = fetch_teams_data(self.league, self.season)
    
    def _map_to_dict(self, team_obj):
        """
        Filtra e mappa i dati del team in un dizionario.
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

    def transform(self):
        """
        Mappa e Trasforma i dati delle squadre
        """

        if not self._extracted_data:
            raise RuntimeError("Extracted data is not available. Run 'extract' method first.")
            
        transformed_teams = []
        for team_obj in self._extracted_data:
            transformed_team = self._map_to_dict(team_obj)
            transformed_teams.append(transformed_team)
        self._transformed_data = transformed_teams

    def load(self):
        """
        Carica i dati trasformati nel database.
        """
        if not self._transformed_data:
            raise RuntimeError("Transformed data is not available. Run 'transform' method first.")
        
        session = self.Session()
        try:
            if not self.historical_data:
                Team.set_all_current_in_serie_a_false(session)

            # Salva i team che non esistono già
            new_teams = [team for team in self._transformed_data if not session.query(Team).filter_by(footballapi_id=team['footballapi_id']).first()]
            Team.save_teams(session, new_teams)

            # Salva i team_details
            team_details = [{
                'team_id': session.query(Team).filter_by(footballapi_id=team['footballapi_id']).first().id,
                'stadium_name': team['stadium_name'],
                'stadium_city': team['stadium_city'],
                'stadium_capacity': team['stadium_capacity'],
                'stadium_img_url': team['stadium_img_url']
            } for team in self._transformed_data]
            TeamDetails.save_team_details(session, team_details)

            if not self.historical_data:
                team_footballapi_ids = [team['footballapi_id'] for team in self._transformed_data]
                Team.update_current_in_serie_a(session, team_footballapi_ids, True)

            logger.info("Teams and team details saved to the database successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {e}")
        finally:
            session.close()

    def run_pipeline(self):
        """
        Esegue la sequenza di estrazione, trasformazione e caricamento dei dati.
        """
        self.extract()
        self.transform()
        self.load()            