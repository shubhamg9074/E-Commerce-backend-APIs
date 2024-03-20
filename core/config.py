import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

class Settings (BaseSettings):

    DB_USER:str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SEVER:str = os.getenv('POSTGRES_SEVER')
    POSTGRES_POST:str = os.getenv('POSTGRES_POST')
    POSTGRES_DB:str = os.getenv('POSTGRES_DB')
    DATABASE_URL:str =f"postgresql://{DB_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SEVER}:{POSTGRES_POST}/{POSTGRES_DB}"


    JWT_SECRET_KEY:str = os.getenv('JWT_SECRET_KEY',"09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    JWT_ALGORITHM:str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',60)

def get_settings()->Settings:
    return Settings()