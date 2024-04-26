from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class db:
    def __init__(self, db_url: str):
        self.offline = False
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = self.engine)
        Base.metadata.create_all(bind = self.engine)

    def connect(self):
        db = self.SessionLocal()
        try:
            return db
        finally:
            db.close()