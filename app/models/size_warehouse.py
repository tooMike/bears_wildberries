from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.size import Size
    from app.models.warehouse import Warehouse


class SizeWarehouseAssociation(Base):
    """Модель для связи размера и склада."""
    __tablename__ = "sizewarehouseassociation"

    size_id: Mapped[int] = mapped_column(
        ForeignKey("size.id"),
        primary_key=True
    )
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouse.id"),
        primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    size: Mapped["Size"] = relationship(
        back_populates="warehouses_associations"
    )
    warehouse: Mapped["Warehouse"] = relationship(
        back_populates="sizes_associations"
    )
