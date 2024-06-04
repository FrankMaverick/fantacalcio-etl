from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
 
class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(50))
    
    team_name_mapping = relationship("TeamNameMapping", back_populates="source")