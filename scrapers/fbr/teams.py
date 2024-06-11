from sqlalchemy import create_engine
import soccerdata as sd
from sqlalchemy.orm import sessionmaker
import logging

from models.source import Source
from models.team import Team
from models.team_name_mappings import TeamNameMapping
from utils.fuzzywuzzy_utils import fuzzy_match_name

logger = logging.getLogger(__name__)

class Teams:
    def __init__(self, db_path, source_name):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.source_name = source_name

    def extract_data(self, league, season):
        """
        Estrae i dati delle squadre per una determinata lega e stagione.
        """
        fbr = sd.FBref(leagues=league, seasons=season)
        return fbr.read_team_season_stats(stat_type="standard")

    def transform_data(self, teams_df):
        """
        Estrae solo il nome della squadra dal DataFrame estratto e restituisce un dizionario.
        """
        team_names_dict = {"team_names": teams_df.reset_index()["team"].tolist()}
        return team_names_dict
    
    def save_data_to_db(self, team_names_dict):
        """
        Salva i nomi delle squadre nel database, associandoli alla sorgente specificata.
        """
        Session = self.Session()
        try:
            source = Source.get_source_by_name(Session, self.source_name)
            if not source:
                raise ValueError(f"Source '{self.source_name}' not found in the database.")

            for team_name in team_names_dict['team_names']:
                # Verifica se il mapping esiste già per la stessa sorgente
                existing_mapping = TeamNameMapping.get_mapping_by_team_and_source(Session, team_name, source.id)
                if existing_mapping:
                    logger.warning(f"Team '{team_name}' already exists in the team_name_mapping table for source '{self.source_name}'.")
                    continue
                
                # Cerca il miglior match fuzzywuzzy tra tutti i nomi dei team esistenti
                best_match, score = fuzzy_match_name(team_name, [team.team_name for team in Team.get_all_teams(Session)])
                if score >= 85:
                    team = Team.get_team_by_name(Session, best_match)
                    if team:
                        TeamNameMapping.save_mapping(Session, {'team_id': team.id, 'source_id': source.id, 'team_name': team_name})
                    else:
                        logger.warning(f"No team found for '{best_match}' in the teams table.")
                else:
                    logger.warning(f"No suitable match found for '{team_name}' in the teams table.")
                    TeamNameMapping.save_mapping(Session, {'team_id': None, 'source_id': source.id, 'team_name': team_name})                
        
            Session.commit()
            logger.info("Team names saved to the database successfully.")
        except Exception as e:
            Session.rollback()
            logger.error(f"Error saving team names to the database: {e}")
        finally:
            Session.close()

