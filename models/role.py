from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    role_principal = Column(String(50), nullable=False, unique=True)
    role_specific = Column(String(50), nullable=True, unique=True)
    role_abbreviation = Column(String(50), nullable=True, unique=True)
    
    players = relationship("Player", back_populates="role") 



    