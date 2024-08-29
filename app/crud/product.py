from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Product


class ProductCRUD(CRUDBase):
    """Класс CRUD для товаров."""

    async def get_product_by_nm_id(
            self,
            nm_id: int,
            session: AsyncSession,
    ) -> int | None:
        """Получение товара по nm_id"""
        product = await session.execute(
            select(self.model).where(
                self.model.nm_id == nm_id
            )
        )
        return product.scalars().first()


product_crud = ProductCRUD(Product)
