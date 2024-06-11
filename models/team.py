from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base import Base
import uuid
import logging

logger = logging.getLogger(__name__)

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
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

    def __repr__(self):
        return f"<Team(uid={self.uid}, team_name='{self.team_name}', team_code='{self.team_code}', team_country='{self.team_country}', team_founded={self.team_founded}, team_logo_url='{self.team_logo_url}', current_in_serie_a={self.current_in_serie_a}, footballapi_id={self.footballapi_id})>"

    @staticmethod
    def get_team_by_id(session, team_id):
        return session.query(Team).filter_by(id=team_id).first()
    
    @staticmethod
    def get_team_by_footballapi_id(session, footballapi_id):
        return session.query(Team).filter_by(footballapi_id=footballapi_id).first()
    
    @staticmethod
    def get_team_by_name(session, team_name):
        return session.query(Team).filter_by(team_name=team_name).first()
    
    @staticmethod
    def get_all_teams(session):
        return session.query(Team).all()
    
    @staticmethod
    def save_teams(session, teams):
        try:
            for team in teams:
                new_team = Team(
                    uid=str(uuid.uuid4()),
                    team_name=team['team_name'],
                    team_code=team['team_code'],
                    team_country=team['team_country'],
                    team_founded=team['team_founded'],
                    team_logo_url=team['team_logo_url'],
                    current_in_serie_a=team['current_in_serie_a'],
                    footballapi_id=team['footballapi_id']
                )
                session.add(new_team)
            session.commit()
            logger.info("Teams saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving teams: {e}")

    @staticmethod
    def update_current_in_serie_a(session, footballapi_ids, status=True):
        session.query(Team).filter(Team.footballapi_id.in_(footballapi_ids)).update(
            {Team.current_in_serie_a: status}, synchronize_session=False)
        session.commit()
        logger.info(f"Updated current_in_serie_a to {status} for teams with FootballApi IDs: {footballapi_ids}")

    @staticmethod
    def set_all_current_in_serie_a_false(session):
        session.query(Team).update({Team.current_in_serie_a: False}, synchronize_session=False)
        session.commit()
        logger.info("Set current_in_serie_a to False for all teams.")
    
    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'team_name': self.team_name,
            'team_code': self.team_code,
            'team_country': self.team_country,
            'team_founded': self.team_founded,
            'team_logo_url': self.team_logo_url,
            'current_in_serie_a': self.current_in_serie_a,
            'footballapi_id': self.footballapi_id
        }