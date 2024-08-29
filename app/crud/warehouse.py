from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Warehouse


class WarehouseCRUD(CRUDBase):
    """Класс CRUD для складов."""

    async def get_warehouse_by_wh(
            self,
            wh: int,
            session: AsyncSession,
    ) -> int | None:
        """Получение склада по wh"""
        product = await session.execute(
            select(self.model).where(
                self.model.wh == wh
            )
        )
        return product.scalars().first()


warehouse_crud = WarehouseCRUD(Warehouse)
