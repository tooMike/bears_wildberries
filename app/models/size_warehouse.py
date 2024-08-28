from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.warehouse import Warehouse
    from app.models.size import Size


class SizeWarehouse(Base):
    """Модель для связи размера и склада."""

    size_id: Mapped[int] = mapped_column(
        ForeignKey("size.id"),
        primary_key=True
    )
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouse.id"),
        primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    size: Mapped["Size"] = relationship(back_populates="warehouses")
    warehouse: Mapped["Warehouse"] = relationship(back_populates="sizes")

    def __repr__(self):
        return self.size
