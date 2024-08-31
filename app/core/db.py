from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

engine: AsyncEngine = create_async_engine(settings.database_url)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_async_session():
    """Генератор асинхронных сессий."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
