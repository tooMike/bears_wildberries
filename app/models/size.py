from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.size_warehouse import SizeWarehouse



class Size(Base):
    """Модель размера."""

    size: Mapped[str] = mapped_column(String, nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="sizes")

    warehouses: Mapped[list["SizeWarehouse"]] = relationship(
        back_populates="sizes"
    )

    def __repr__(self):
        return self.size
