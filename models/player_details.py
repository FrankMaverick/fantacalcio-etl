from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
import uuid
import logging

logger = logging.getLogger(__name__)

class PlayerDetails(Base):
    __tablename__ = 'player_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    player_id = Column(Integer, ForeignKey('players.id'), unique=True)
    height = Column(Float)
    weight = Column(Float)
    birth_date = Column(Date)
    nationality = Column(String(100))
    img_url = Column(String)

    player = relationship("Player", back_populates="player_detail")

    def __init__(self, player_id, height, weight, birth_date, nationality, img_url):
        self.player_id = player_id
        self.height = height
        self.weight = weight
        self.birth_date = birth_date
        self.nationality = nationality
        self.img_url = img_url

    def __repr__(self):
        return f"""<PlayerDetails(
            uid={self.uid}, 
            player_id={self.player_id}, 
            height={self.height}, 
            weight={self.weight}, 
            birth_date={self.birth_date}, 
            nationality='{self.nationality}', 
            img_url='{self.img_url}')>"""

    @staticmethod
    def get_details_by_player_id(session, player_id):
        return session.query(PlayerDetails).filter_by(player_id=player_id).first()
    
    @staticmethod
    def get_details_by_id(session, detail_id):
        return session.query(PlayerDetails).filter_by(id=detail_id).first()

    @staticmethod
    def save_player_details(session, player_details_list):
        try:
            for details in player_details_list:
                new_details = PlayerDetails(
                    player_id=details['player_id'],
                    height=details['height'],
                    weight=details['weight'],
                    birth_date=details['birth_date'],
                    nationality=details['nationality'],
                    img_url=details['img_url']
                )
                session.add(new_details)
            session.commit()
            logger.info("Player details saved successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving player details: {e}")

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'player_id': self.player_id,
            'height': self.height,
            'weight': self.weight,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality,
            'img_url': self.img_url
        }