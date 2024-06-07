from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base

class PlayerNameMapping(Base):
    __tablename__ = 'player_name_mappings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    player_name = Column(String(255))
    
    player = relationship("Player", back_populates="player_name_mappings")
    source = relationship("Source", back_populates="player_name_mapping")

    __table_args__ = (UniqueConstraint('source_id', 'player_name', name='_source_player_name_uc'),)
