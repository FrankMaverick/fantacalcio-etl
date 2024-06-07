from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    team_name = Column(String(50))
    team_code = Column(String(10))
    team_country = Column(String(50))
    team_founded = Column(Integer)
    team_logo_url = Column(String(255))
    current_in_serie_a = Column(Boolean)
    footballapi_id = Column(Integer, unique=True)

    players = relationship("Player", back_populates="team")
    details = relationship("TeamDetails", back_populates="team")
    team_name_mappings = relationship("TeamNameMapping", back_populates="team")