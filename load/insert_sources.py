from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sources import Source
from config import DB_PATH

import logging
logger = logging.getLogger(__name__)

def insert_source(source_name):
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Verifica se la fonte è già presente nella tabella
        existing_source = session.query(Source).filter_by(source_name=source_name).first()
        if existing_source:
            logger.warning(f"Source '{source_name}' already exists in the source table.")
        else:
            # Inserisci la nuova fonte
            new_source = Source(source_name=source_name)
            session.add(new_source)
            session.commit()
            logger.info(f"Source '{source_name}' successfully inserted into the source table.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
    finally:
        session.close()
