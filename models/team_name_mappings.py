from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class TeamNameMapping(Base):
    __tablename__ = 'team_name_mappings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    team_name = Column(String(255))
    
    team = relationship("Team", back_populates="team_name_mappings")
    source = relationship("Source", back_populates="team_name_mapping")