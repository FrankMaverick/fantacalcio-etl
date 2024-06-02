from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    display_name = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    team_id = Column(Integer, ForeignKey('teams.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    serie_a_player = Column(Boolean)
    
    team = relationship("Team", back_populates="players")
    role = relationship("Role", back_populates="players")

    player_detail = relationship("PlayerDetails", back_populates="player") 
