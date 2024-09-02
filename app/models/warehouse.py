from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.size import Size
    from app.models.size_warehouse import SizeWarehouseAssociation


class Warehouse(Base):
    """Модель склада."""

    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wh: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    sizes: Mapped[list["Size"]] = relationship(
        secondary="sizewarehouseassociation",
        back_populates="warehouses",
        viewonly=True
    )
    sizes_associations: Mapped[
        list["SizeWarehouseAssociation"]] = relationship(
        back_populates="warehouse"
    )

    def __repr__(self):
        return str(self.wh)
