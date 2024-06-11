import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base
import logging

logger = logging.getLogger(__name__)

class PlayerNameMapping(Base):
    __tablename__ = 'player_name_mappings'
    __table_args__ = (
        UniqueConstraint('player_id', 'source_id', name='unique_player_source'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    player_id = Column(Integer, ForeignKey('players.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    player_name = Column(String(100))
    
    player = relationship("Player", back_populates="player_name_mappings")
    source = relationship("Source", back_populates="player_name_mapping")
    
    @staticmethod
    def get_mapping_by_player_and_source(session, player_name, source_id):
        return session.query(PlayerNameMapping).filter_by(player_name=player_name, source_id=source_id).first()
    
    @staticmethod
    def save_mapping(session, mapping_data):
        try:
            new_mapping = PlayerNameMapping(
                player_id=mapping_data['player_id'],
                source_id=mapping_data['source_id'],
                player_name=mapping_data['player_name']
            )
            session.add(new_mapping)
            session.commit()
            logger.info("Player name mapping saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving player name mapping: {e}")
