from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing_extensions import AsyncGenerator

from .config import get_settings


settings = get_settings()
engine = create_async_engine(
    settings.sqlalchemy_database_url,
    poolclass=NullPool,
)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, expire_on_commit=False, autoflush=False, bind=engine
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронная функция, которая подключается к сессии
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

DBSession = AsyncSessionLocal