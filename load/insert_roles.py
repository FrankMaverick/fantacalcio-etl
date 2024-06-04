import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.role import Role
from models.player import Player
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def translate_role(role):
    role = role.lower()  # Converte il testo a minuscolo per evitare problemi di capitalizzazione
    if role == "goalkeeper":
        return "Portiere"
    elif role == "defender":
        return "Difensore"
    elif role == "midfielder":
        return "Centrocampista"
    elif role == "attacker":
        return "Attaccante"
    else:
        return None


def insert_roles(player_details_df):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _, row in player_details_df.iterrows():
            # Cerca il giocatore utilizzando il campo footballapi_id
            player = session.query(Player).filter_by(footballapi_id=row['player_id']).first()
            
            if player:
                role = Role(
                    role_principal = translate_role(row['player_position']),
                    role_specific=None,
                    role_abbreviation=None
                )
                session.add(role)
            else:
                logger.error(f"Player with footballapi_id '{row['player_id']}' not found in the database.")
        
        session.commit()
        logger.info("Player roles inserted successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
