from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player import Player
from models.team import Team
from models.sources import Source
from models.player_name_mappings import PlayerNameMapping
from models.team_name_mappings import TeamNameMapping
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

def get_full_name(display_name, first_name):
    """
    Sostituisce l'iniziale puntata nel display_name con il first_name, se corrisponde.
    Altrimenti il primo first_name. Se non c'è il punto, tutto il display_name
    """
    if '. ' in display_name:
        initial, last_name = display_name.split('. ', 1)
        for name in first_name.split():
            if name.startswith(initial):
                return f"{name} {last_name}"
        return f"{first_name.split()[0]} {last_name}"
    return display_name

def insert_player_name_mappings(player_names_df, source_name):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        source_id = get_source_id(session, source_name)
        if source_id is None:
            logger.warning(f"Source name {source_name} not configured")
            return
        
        #TODO: ci sono giocatori che hanno 2 team nel df, giocatori che sono passati da un team all'altro durante la stagione (es. Zapata)
        for _, row in player_names_df.iterrows():
            player_name = row['player']
            team_name = row['team']

            # Verifica se il nome del giocatore è già presente nella tabella di mapping
            existing_mapping = session.query(PlayerNameMapping).filter_by(player_name=player_name, source_id=source_id).first()

            if existing_mapping:
                logger.warning(f"Player '{player_name}' already exists in the player_name_mappings table for source '{source_name}'.")
                continue
            
            # Ottieni il team_id corrispondente al team_name nella tabella team_name_mappings per la stessa source
            team_mapping = session.query(TeamNameMapping).filter_by(team_name=team_name, source_id=source_id).first()
            if not team_mapping:
                logger.warning(f"No team mapping found for team '{team_name}' and source '{source_name}'. Skipping player '{player_name}'.")
                continue

            team_id = team_mapping.team_id

            # Ottieni tutti i giocatori del team specificato
            players = session.query(Player).filter_by(team_id=team_id).all()
            all_player_names = [get_full_name(player.display_name, player.first_name) for player in players]

            # Cerca il miglior match fuzzywuzzy tra i nomi dei giocatori del team specificato
            best_match, score = fuzzy_match_name(player_name, all_player_names)
            logger.debug(f"Best match for '{player_name}' is '{best_match}' with score {score}")

            if score >= 85:
                matched_player = next((p for p in players if get_full_name(p.display_name, p.first_name) == best_match), None)
                if matched_player:
                    if existing_mapping:
                        # Update existing mapping
                        existing_mapping.player_id = matched_player.id
                    else:
                        # Add new mapping
                        new_mapping = PlayerNameMapping(
                            player_id=matched_player.id,
                            source_id=source_id,
                            player_name=player_name
                        )
                        session.add(new_mapping)
                else:
                    logger.warning(f"No player found for '{best_match}' in the players table.")
            else:
                if existing_mapping:
                    # Update existing mapping
                    existing_mapping.player_id = None
                else:
                    # Add new mapping without player_id
                    new_mapping = PlayerNameMapping(
                        player_id=None,
                        source_id=source_id,
                        player_name=player_name
                    )
                    session.add(new_mapping)

        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
