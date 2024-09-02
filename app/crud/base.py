from typing import List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

S = TypeVar('S', bound=Base)


class CRUDBase:
    """Базовый класс для CRUD операций."""

    def __init__(self, model: Type[S]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[S]:
        """Получение 1 объекта."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[S]:
        """Получение списка объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
