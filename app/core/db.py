from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (async_sessionmaker, AsyncEngine,
                                    AsyncSession, create_async_engine)
from sqlalchemy.orm import (declarative_base, declared_attr, Mapped,
                            mapped_column)

from app.core.config import settings

#
# class PreBase:
#     """Базовый класс для всех моделей."""
#
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)


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
