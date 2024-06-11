from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.source import Source
import logging

logger = logging.getLogger(__name__)

class ScraperFBR:
    def __init__(self, db_path):
        self.db_engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.db_engine)

    def add_source(self, source_name):
        """
        Aggiunge una nuova sorgente al database.
        """
        session = self.Session()
        try:
            Source.save_source(session, source_name)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            session.close()
