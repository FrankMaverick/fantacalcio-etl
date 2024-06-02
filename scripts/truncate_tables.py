from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import DB_PATH

def truncate_tables():
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    meta = MetaData(bind=engine)
    meta.reflect()

    for table in reversed(meta.sorted_tables):
        session.execute(f'DELETE FROM {table.name}')
        session.execute(f'DELETE FROM sqlite_sequence WHERE name="{table.name}"')  # Reset AUTOINCREMENT
        print(f'Table {table.name} truncated.')
    
    session.commit()
    session.close()

if __name__ == "__main__":
    truncate_tables()
