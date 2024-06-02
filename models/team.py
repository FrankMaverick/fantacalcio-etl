from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    team_name = Column(String(255))
    team_code = Column(String(10))
    team_country = Column(String(100))
    team_founded = Column(Integer)
    #team_national = Column(Boolean)
    team_logo_url = Column(String(255))
    current_in_serie_a = Column(Boolean)

    players = relationship("Player", back_populates="team")
    details = relationship("TeamDetails", back_populates="team")