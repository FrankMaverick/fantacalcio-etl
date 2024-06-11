import uuid
from sqlalchemy import create_engine
import soccerdata as sd
from sqlalchemy.orm import sessionmaker
import logging

from models.source import Source
from models.player import Player
from models.player_name_mappings import PlayerNameMapping
from models.team_name_mappings import TeamNameMapping
from utils.fuzzywuzzy_utils import fuzzy_match_name

logger = logging.getLogger(__name__)

class Players:
    def __init__(self, db_path, source_name):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)
        self.source_name = source_name

    def extract_data(self, league, season):
        """
        Estrae i dati dei giocatori per una determinata lega e stagione.
        """
        fbr = sd.FBref(leagues=league, seasons=season)
        return fbr.read_player_season_stats(stat_type="standard")

    def transform_data(self, players_df):
        """
        Estrae il nome del giocatore e il nome della squadra per ogni riga del DataFrame estratto e restituisce una lista di dizionari.
        """
        player_team_list = []
        player_team_data = players_df.reset_index()
        for _, row in player_team_data.iterrows():
            player_team_dict = {
                "player": row["player"].tolist()[0],
                "team": row["team"].tolist()[0]
            }
            player_team_list.append(player_team_dict)
        return player_team_list

    def save_data_to_db(self, player_team_list):
        """
        Salva i nomi dei giocatori e delle squadre nel database, associandoli alla sorgente specificata.
        """
        Session = self.Session()
        try:
            source = Source.get_source_by_name(Session, self.source_name)
            if not source:
                raise ValueError(f"Source '{self.source_name}' not found in the database.")

            source_id = source.id

            for item in player_team_list:
                player_name = item["player"]
                team_name = item["team"]

                print(player_name)
                print(team_name)

                # Verifica se il nome del giocatore è già presente nella tabella di mapping
                existing_mapping = PlayerNameMapping.get_mapping_by_player_and_source(Session, player_name, source_id)

                if existing_mapping:
                    logger.warning(f"Player '{player_name}' already exists in the player_name_mappings table for source '{self.source_name}'.")
                    continue
                
                # Ottieni il team_id corrispondente al team_name nella tabella team_name_mappings per la stessa source
                team_mapping = TeamNameMapping.get_mapping_by_team_and_source(Session, team_name, source_id)
                if not team_mapping:
                    logger.warning(f"No team mapping found for team '{team_name}' and source '{self.source_name}'. Skipping player '{player_name}'.")
                    continue

                team_id = team_mapping.team_id

                # Ottieni tutti i giocatori del team specificato
                players = Player.get_players_by_team_id(Session, team_id)
                all_player_names = [self._get_full_name(player.display_name, player.first_name) for player in players]

                # Cerca il miglior match fuzzywuzzy tra i nomi dei giocatori del team specificato
                best_match, score = fuzzy_match_name(player_name, all_player_names)
                logger.debug(f"Best match for '{player_name}' is '{best_match}' with score {score}")

                if score >= 85:
                    matched_player = next((p for p in players if self._get_full_name(p.display_name, p.first_name) == best_match), None)
                    if matched_player:
                        if existing_mapping:
                            # Update existing mapping
                            existing_mapping.player_id = matched_player.id
                        else:
                            # Add new mapping
                            PlayerNameMapping.save_mapping(Session, {'player_id': matched_player.id, 'source_id': source_id, 'player_name': player_name})
                    else:
                        logger.warning(f"No player found for '{best_match}' in the players table.")
                else:
                    if existing_mapping:
                        # Update existing mapping
                        existing_mapping.player_id = None
                    else:
                        # Add new mapping without player_id
                        PlayerNameMapping.save_mapping(Session, {'player_id': None, 'source_id': source_id, 'player_name': player_name})

            Session.commit()
            logger.info("Player names saved to the database successfully.")
        except Exception as e:
            Session.rollback()
            logger.error(f"Error saving player names to the database: {e}")
        finally:
            Session.close()


    def _get_full_name(self, display_name, first_name):
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