import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.role import Role
from models.player import Player
from config import DB_PATH
from utils.helpers import generate_uid

import logging
logger = logging.getLogger(__name__)

def translate_role(role):
    role = role.lower()
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

def insert_roles(player_details_df, HISTORICAL_DATA):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _, row in player_details_df.iterrows():
            # Cerca il giocatore utilizzando il campo footballapi_id
            player = session.query(Player).filter_by(footballapi_id=row['player_id']).first()
            
            if player:
                if HISTORICAL_DATA:
                    role = row['games_position']
                else:
                    role = row['player_position']
                role_principal = translate_role(role)
                
                # Controlla se il ruolo esiste già
                role = session.query(Role).filter_by(role_principal=role_principal).first()
                if not role:
                    role = Role(
                        uid=generate_uid(),
                        role_principal=role_principal,
                        role_specific=None,
                        role_abbreviation=None
                    )
                    session.add(role)
                    session.commit()  # Commit per ottenere l'id del ruolo
                
                # Aggiorna il role_id del giocatore
                player.role_id = role.id
                session.commit()
            else:
                logger.error(f"Player with footballapi_id '{row['player_id']}' not found in the database.")
        
        logger.info("Player roles inserted and updated successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
