from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from models.base import Base

class PlayerDetails(Base):
    __tablename__ = 'player_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), unique=True)
    height = Column(Float)
    weight = Column(Float)
    birth_date = Column(Date)
    nationality = Column(String(100))
    img_url = Column(String)

    player = relationship("Player", back_populates="player_detail")