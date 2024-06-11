import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base
import logging

logger = logging.getLogger(__name__)

class TeamNameMapping(Base):
    __tablename__ = 'team_name_mappings'
    __table_args__ = (
        UniqueConstraint('team_id', 'source_id', name='unique_team_source'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    team_name = Column(String(50))
    
    team = relationship("Team", back_populates="team_name_mappings")
    source = relationship("Source", back_populates="team_name_mapping")
    
    
    @staticmethod
    def get_mapping_by_team_and_source(session, team_name, source_id):
        return session.query(TeamNameMapping).filter_by(team_name=team_name, source_id=source_id).first()
    
    @staticmethod
    def save_mapping(session, mapping_data):
        try:
            new_mapping = TeamNameMapping(
                team_id=mapping_data['team_id'],
                source_id=mapping_data['source_id'],
                team_name=mapping_data['team_name']
            )
            session.add(new_mapping)
            session.commit()
            logger.info("Team name mapping saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving team name mapping: {e}")
