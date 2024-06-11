import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
import logging

logger = logging.getLogger(__name__)

class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    source_name = Column(String(50), unique=True, nullable=False)
    
    team_name_mapping = relationship("TeamNameMapping", back_populates="source")
    player_name_mapping = relationship("PlayerNameMapping", back_populates="source")
    
    def __repr__(self):
        return f"<Source(uid={self.uid}, source_name='{self.source_name}')>"

    @staticmethod
    def get_source_by_id(session, source_id):
        return session.query(Source).filter_by(id=source_id).first()
    
    @staticmethod
    def get_source_by_name(session, name):
        return session.query(Source).filter_by(source_name=name).first()
    
    @staticmethod
    def get_all_sources(session):
        return session.query(Source).all()
    
    @staticmethod
    def save_source(session, source_name):
        try:
            new_source = Source(
                source_name=source_name
            )
            session.add(new_source)
            session.commit()
            logger.info(f"Source {source_name} saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving source: {e}")

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'source_name': self.source_name
        }
