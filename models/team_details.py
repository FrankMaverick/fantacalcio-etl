from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class TeamDetails(Base):
    __tablename__ = 'team_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'), unique=True, nullable=False)
    stadium_name = Column(String)
    stadium_city = Column(String)
    stadium_capacity = Column(Integer)
    stadium_image_url = Column(String)

    team = relationship("Team", back_populates="details")