import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")

class Settings(BaseSettings):
    """
    Класс для получения настроек базы данных для установления соединения с ней
    """
    sqlalchemy_database_url: str = (
        f"postgresql+asyncpg://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Функция получает настройки из класса Settings
    """
    return Settings()