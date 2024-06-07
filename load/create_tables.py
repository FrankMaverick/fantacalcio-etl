from sqlalchemy import create_engine
from models.base import Base
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