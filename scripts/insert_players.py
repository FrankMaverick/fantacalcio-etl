import uuid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.player import Player
from models.player_details import PlayerDetails
from config import DB_PATH

def generate_uuid():
    return str(uuid.uuid4())

def insert_players(session, players_df):
    for index, player in players_df.iterrows():
        player_data = Player(
            uid=generate_uuid(),
            display_name=player['player_name'],
            first_name=player['player_firstname'],
            last_name=player['player_lastname']
        )
        session.add(player_data)
    session.commit()

def insert_player_details(session, players_details_df):
    for index, player_details in players_details_df.iterrows():
        display_name = player_details['display_name']
        player = session.query(Player).filter_by(display_name=display_name).first()
        
        if player:
            player_details_data = PlayerDetails(
                uid=generate_uuid(),
                player_id=player.id,
                height=player_details['height'],
                weight=player_details['weight'],
                birth_date=player_details['birth_date'],
                nationality=player_details['nationality'],
                img_url=player_details['img_url']
            )
            session.add(player_details_data)
        else:
            print(f"Player with display_name {display_name} not found in players table.")
    session.commit()

def main():
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    players_df = pd.read_csv('data/players.csv')
    players_details_df = pd.read_csv('data/player_details.csv')

    insert_players(session, players_df)
    insert_player_details(session, players_details_df)

    session.close()

if __name__ == "__main__":
    main()
