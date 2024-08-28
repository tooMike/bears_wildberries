from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Базовая схема товара."""

    nm_id: int = Field(..., ge=0)
    current_price: int = Field(..., ge=0)
    sum_quantity: int = Field(..., ge=0)


class ProductRead(ProductBase):
    """Схема для получения информации о товаре."""

    quantity_by_sizes: list[]

