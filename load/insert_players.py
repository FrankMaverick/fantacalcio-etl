import uuid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player import Player
from models.team import Team  # Importa il modello Team
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def generate_uuid():
    return str(uuid.uuid4())

def insert_players(players_df, historical_data=False):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not historical_data:
            # Set serie_a_player to False and team_id to None for all existing players 
            session.query(Player).update({Player.serie_a_player: False, Player.team_id: None})
            session.commit()

        for _, row in players_df.iterrows():
            # Cerca l'ID del team utilizzando il team_id di football_api presente nel DataFrame e nella tabella Teams
            team = session.query(Team).filter_by(footballapi_id=row['team_id']).first()
            if team:
                team_id = team.id
            else:
                logger.error(f"Team '{row['team_name']}' not found in the database.")
                continue
            
            player_data = {
                'uid': generate_uuid(),
                'display_name': row['player_name'],
                'first_name': row['player_firstname'],
                'last_name': row['player_lastname'],
                'team_id': team_id,
                'role_id': None,  # Null at the moment
                'serie_a_player': True if not historical_data else None,
                'footballapi_id': row['player_id']
            }

            player = session.query(Player).filter_by(footballapi_id=row['player_id']).first()
            if player:
                # Update existing player
                player.serie_a_player = True if not historical_data else None
                player.team_id = team_id
            else:
                # Insert new player
                new_player = Player(**player_data)
                session.add(new_player)

        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()