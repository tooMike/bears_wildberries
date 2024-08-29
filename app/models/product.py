from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.size import Size


class Product(Base):
    """Модель продукта."""
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nm_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    current_price: Mapped[int] = mapped_column(Integer, nullable=False)
    sum_quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    sizes: Mapped[list["Size"]] = relationship(back_populates="product")

    def __repr__(self):
        return str(self.nm_id)
