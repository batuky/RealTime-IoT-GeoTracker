from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
class DatabaseSessionManager:
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


def get_db():
    with DatabaseSessionManager() as db:
        yield db

def init_db():
    Base.metadata.create_all(bind=engine)

def close_db():
    engine.dispose()