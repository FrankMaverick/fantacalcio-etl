from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    source_name = Column(String(50))
    
    team_name_mapping = relationship("TeamNameMapping", back_populates="source")
    player_name_mapping = relationship("PlayerNameMapping", back_populates="source")
