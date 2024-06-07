import uuid
import pandas as pd
from sqlalchemy import create_engine, insert, update
from sqlalchemy.orm import sessionmaker
from config import DB_PATH
from models.base import Base
from models.team import Team
from utils.helpers import generate_uid

import logging
logger = logging.getLogger(__name__)

def insert_teams(df_teams, historical_data=False):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not historical_data:
            # Set current_in_serie_a to False for all existing teams
            session.query(Team).update({Team.current_in_serie_a: False})
            session.commit()

        for _, row in df_teams.iterrows():
            team_data = {
                'uid': generate_uid(),
                'footballapi_id': row['team_id'],
                'team_name': row['team_name'],
                'team_code': row['team_code'],
                'team_country': row['team_country'],
                'team_founded': row['team_founded'],
                'team_logo_url': row['team_logo'],
                'current_in_serie_a': True if not historical_data else None
            }

            team = session.query(Team).filter_by(footballapi_id=row['team_id']).first()
            if team:
                # Update existing team
                team.current_in_serie_a = True if not historical_data else None
            else:
                # Insert new team
                new_team = Team(**team_data)
                session.add(new_team)

        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()