from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.team_name_mappings import TeamNameMapping
from models.team import Team
from models.sources import Source
from utils.fuzzywuzzy_utils import fuzzy_match_name
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def get_source_id(session, source_name):
    source = session.query(Source).filter_by(source_name=source_name).first()
    if source:
        return source.id
    else:
        logger.error(f"No source found for '{source_name}'")
        return None

def insert_team_name_mappings(team_names_df, source_name):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        source_id = get_source_id(session, source_name)
        if source_id is None:
            logger.warning(f"Source name {source_name} not configured")
            return
        
        # Ottieni tutti i nomi dei team presenti nella tabella teams
        all_team_names = [team.team_name for team in session.query(Team).all()]

        for _, row in team_names_df.iterrows():
            # Verifica se il nome del team è già presente nella tabella di mapping
            existing_mapping = session.query(TeamNameMapping).filter_by(team_name=row['team'], source_id=source_id).first()
            if existing_mapping:
                logger.warning(f"Team '{row['team']}' already exists in the team_name_mapping table for source '{source_name}'.")
                continue
            
            # Cerca il miglior match fuzzywuzzy tra tutti i nomi dei team esistenti
            best_match, score = fuzzy_match_name(row['team'], all_team_names)
            if score >= 85:
                team = session.query(Team).filter_by(team_name=best_match).first()
                if team:
                    new_mapping = TeamNameMapping(
                        team_id=team.id,                        
                        source_id=source_id,
                        team_name=row['team']
                    )
                    session.add(new_mapping)
                else:
                    logger.warning(f"No team found for '{best_match}' in the teams table.")
            else:
                logger.warning(f"No suitable match found for '{row['team']}' in the teams table.")
                new_mapping = TeamNameMapping(
                    team_id=None,
                    source_id=source_id,
                    team_name=row['team']
                )
                session.add(new_mapping)                
        
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()

