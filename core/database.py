import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from core.config import get_settings


# URL_DATABASE ='postgresql://postgres:shubh123@localhost:5432/postgres'

settings=get_settings()

engine = create_engine(settings.DATABASE_URL,echo=True)

sessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()