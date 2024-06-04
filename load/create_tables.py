from sqlalchemy import create_engine
from models.base import Base
from models.team import Team
from models.player import Player
from models.player_details import PlayerDetails
from models.role import Role
from models.team_details import TeamDetails
from sqlalchemy.exc import SQLAlchemyError
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def create_tables():
    try:
        engine = create_engine(DB_PATH)
        Base.metadata.create_all(engine)
        logger.debug("Tables created")
    except SQLAlchemyError as e:
        logger.error("Error during tables creation: %s", e)

if __name__ == "__main__":
    create_tables()