from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.team import Team
from models.team_details import TeamDetails
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def insert_team_details(df_team_details):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Ottieni un dizionario di mapping footballapi_id -> ID del team dalla tabella teams
        team_footapi_id_mapping = {team.footballapi_id: team.id for team in session.query(Team).all()}
        
        for _, row in df_team_details.iterrows():
            # Ottieni l'ID del team dal dizionario di mapping usando il nome del team dal DataFrame
            team_id = team_footapi_id_mapping.get(row['team_id'])

            if team_id:
                # Verifica se esiste già un record per questo team nei team_details
                existing_team_details = session.query(TeamDetails).filter_by(team_id=team_id).first()
                
                if existing_team_details:
                    # Aggiorna i dettagli del team esistenti
                    existing_team_details.stadium_name = row['venue_name']
                    existing_team_details.stadium_city = row['venue_city']
                    existing_team_details.stadium_capacity = row['venue_capacity']
                    existing_team_details.stadium_image_url = row['venue_image']
                else:
                    # Inserisci nuovi dettagli del team
                    team_details = TeamDetails(
                        team_id=team_id,
                        stadium_name=row['venue_name'],
                        stadium_city=row['venue_city'],
                        stadium_capacity=row['venue_capacity'],
                        stadium_image_url=row['venue_image']
                    )
                    session.add(team_details)
            else:
                logger.error(f"Team '{row['team_id']}' not found in the database.")

        session.commit()
        logger.info("Team details inserted successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
