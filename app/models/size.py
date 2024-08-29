from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.size_warehouse import SizeWarehouseAssociation
    from app.models.warehouse import Warehouse


class Size(Base):
    """Модель размера."""
    __tablename__ = "size"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    size: Mapped[str] = mapped_column(String, nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="sizes")

    warehouses: Mapped[list["Warehouse"]] = relationship(
        secondary="sizewarehouseassociation",
        back_populates="sizes",
        viewonly=True
    )
    warehouses_associations: Mapped[
        list["SizeWarehouseAssociation"]] = relationship(
        back_populates="size"
    )

    def __repr__(self):
        return self.size
