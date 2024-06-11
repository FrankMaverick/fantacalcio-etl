from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
import logging
import uuid

logger = logging.getLogger(__name__)

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    display_name = Column(String(100), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role_principal = Column(String(50))    
    team_id = Column(Integer, ForeignKey('teams.id'))
    current_in_serie_a = Column(Boolean)
    footballapi_id = Column(Integer, unique=True)
    #created_at = Column(DateTime, server_default=func.now())
    #updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())    
    
    team = relationship("Team", back_populates="players")
    player_detail = relationship("PlayerDetails", back_populates="player", uselist=False)
    #player_detail = relationship("PlayerDetails", back_populates="player")
    #player_name_mappings = relationship("PlayerNameMapping", back_populates="player")
    
    def __init__(self, display_name, first_name, last_name, team_id, role_principal, current_in_serie_a, footballapi_id):
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.team_id = team_id
        self.role_principal = role_principal
        self.current_in_serie_a = current_in_serie_a
        self.footballapi_id = footballapi_id

    def __repr__(self):
        return f"""<Player(
            uid={self.uid}, 
            display_name='{self.display_name}', 
            first_name='{self.first_name}', 
            last_name='{self.last_name}', 
            team_id={self.team_id}, 
            role_id={self.role_id}, 
            current_in_serie_a={self.current_in_serie_a}, 
            footballapi_id={self.footballapi_id})>"""

    @staticmethod
    def get_player_by_id(session, player_id):
        return session.query(Player).filter_by(id=player_id).first()
    
    @staticmethod
    def get_players_by_team_id(session, team_id):
        return session.query(Player).filter_by(team_id=team_id).all()

    @staticmethod
    def get_player_by_footballapi_id(session, footballapi_id):
        return session.query(Player).filter_by(footballapi_id=footballapi_id).first()
    
    @staticmethod
    def get_all_players(session):
        return session.query(Player).all()
    
    @staticmethod
    def save_players(session, players_list):
        try:
            for player in players_list:
                new_player = Player(
                    display_name=player['display_name'],
                    first_name=player['first_name'],
                    last_name=player['last_name'],
                    team_id=player['team_id'],
                    role_principal=player['role_principal'],
                    current_in_serie_a=player['current_in_serie_a'],
                    footballapi_id=player['footballapi_id']
                )
                session.add(new_player)
            session.commit()
            logger.info("Players saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving players: {e}")

    @staticmethod
    def update_current_in_serie_a(session, footballapi_ids, status=True):
        session.query(Player).filter(Player.footballapi_id.in_(footballapi_ids)).update(
            {Player.current_in_serie_a: status}, synchronize_session=False)
        session.commit()
        logger.info(f"Updated current_in_serie_a to {status} for players with FootballApi IDs: {footballapi_ids}")

    @staticmethod
    def set_all_current_in_serie_a_false(session):
        session.query(Player).update({Player.current_in_serie_a: False}, synchronize_session=False)
        session.commit()
        logger.info("Set current_in_serie_a to False for all players.")            

    @staticmethod
    def set_all_team_id_null(session):
        session.query(Player).update({Player.team_id: None}, synchronize_session=False)
        session.commit()
        logger.info("Set current_in_serie_a to False for all players.")           

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'display_name': self.display_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'team_id': self.team_id,
            'role_id': self.role_id,
            'current_in_serie_a': self.current_in_serie_a,
            'footballapi_id': self.footballapi_id,
            #'created_at': self.created_at.isoformat(),
            #'updated_at': self.updated_at.isoformat()
        }