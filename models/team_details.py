from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
import uuid

class TeamDetails(Base):
    __tablename__ = 'team_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id'), unique=True, nullable=False)
    stadium_name = Column(String(255))
    stadium_city = Column(String(100))
    stadium_capacity = Column(Integer)
    stadium_img_url = Column(String(255))

    team = relationship("Team", back_populates="details")

    def __repr__(self):
        return f"<TeamDetails(uid={self.uid}, team_id={self.team_id}, stadium_name='{self.stadium_name}', stadium_city='{self.stadium_city}', stadium_capacity={self.stadium_capacity}, stadium_img_url='{self.stadium_img_url}')>"

    @staticmethod
    def get_team_details_by_id(session, details_id):
        return session.query(TeamDetails).filter_by(id=details_id).first()
    
    @staticmethod
    def get_team_details_by_team_id(session, team_id):
        return session.query(TeamDetails).filter_by(team_id=team_id).first()
    
    @staticmethod
    def get_all_team_details(session):
        return session.query(TeamDetails).all()
    
    @staticmethod
    def save_team_details(session, team_details):
        for details in team_details:
            existing_details = session.query(TeamDetails).filter_by(team_id=details['team_id']).first()
            if existing_details:
                existing_details.stadium_name = details['stadium_name']
                existing_details.stadium_city = details['stadium_city']
                existing_details.stadium_capacity = details['stadium_capacity']
                existing_details.stadium_img_url = details['stadium_img_url']
            else:
                new_details = TeamDetails(
                    uid=str(uuid.uuid4()),
                    team_id=details['team_id'],
                    stadium_name=details['stadium_name'],
                    stadium_city=details['stadium_city'],
                    stadium_capacity=details['stadium_capacity'],
                    stadium_img_url=details['stadium_img_url']
                )
                session.add(new_details)
        session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'team_id': self.team_id,
            'stadium_name': self.stadium_name,
            'stadium_city': self.stadium_city,
            'stadium_capacity': self.stadium_capacity,
            'stadium_img_url': self.stadium_img_url
        }
