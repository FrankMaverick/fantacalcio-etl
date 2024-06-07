from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class TeamDetails(Base):
    __tablename__ = 'team_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), unique=True, nullable=False)
    stadium_name = Column(String(255))
    stadium_city = Column(String(100))
    stadium_capacity = Column(Integer)
    stadium_img_url = Column(String(255))

    team = relationship("Team", back_populates="details")