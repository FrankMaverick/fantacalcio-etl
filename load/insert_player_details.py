import re
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player_details import PlayerDetails
from models.player import Player
from config import DB_PATH
from utils.helpers import generate_uid

import logging
logger = logging.getLogger(__name__)

def transform_value(value):
    """Rimuove tutti i caratteri non numerici da una stringa e restituisce un intero."""
    if value is not None:
        numeric_value = re.sub(r'\D', '', value)
        if numeric_value:
            return int(numeric_value)
    return None

def parse_date(date_str):
    """Converte una stringa nel formato 'YYYY-MM-DD' in un oggetto datetime.date."""
    if date_str is not None:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return None

def insert_player_details(player_details_df):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _, row in player_details_df.iterrows():
            # Cerca il giocatore utilizzando il campo footballapi_id
            player = session.query(Player).filter_by(footballapi_id=row['player_id']).first()
            
            if player:
                player_details = PlayerDetails(
                    uid=generate_uid(),
                    player_id=player.id,
                    height=transform_value(row['player_height']),
                    weight=transform_value(row['player_weight']),
                    birth_date=parse_date(row['player_birth_date']),
                    nationality=row['player_birth_country'],
                    img_url=row['player_photo']
                )
                session.add(player_details)
            else:
                logger.error(f"Player with footballapi_id '{row['player_id']}' not found in the database.")
        
        session.commit()
        logger.info("Player details inserted successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
