from sqlalchemy import create_engine, MetaData
from models.base import Base
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)


def drop_tables():
    logger.info("Dropping all tables...")
    engine = create_engine(DB_PATH)
    Base.metadata.drop_all(bind=engine)
    logger.info("Done")

if __name__ == "__main__":
    drop_tables()