from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Product, Size, SizeWarehouseAssociation


class ProductCRUD(CRUDBase):
    """Класс CRUD для товаров."""

    async def get_product_by_nm_id(
            self,
            nm_id: int,
            session: AsyncSession,
    ) -> int | None:
        """Получение товара по nm_id"""
        product = await session.execute(
            select(Product).where(
                Product.nm_id == nm_id
            ).options(
                joinedload(
                    Product.sizes
                ).joinedload(
                    Size.warehouses_associations
                ).joinedload(
                    SizeWarehouseAssociation.warehouse
                )
            )
        )
        return product.scalars().first()


product_crud = ProductCRUD(Product)
