from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.size_warehouse import SizeWarehouse


class Warehouse(Base):
    """Модель склада."""

    wh: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    sizes: Mapped[list["SizeWarehouse"]] = relationship(
        back_populates="warehouses"
    )

    def __repr__(self):
        return self.wh
