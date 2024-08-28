from pydantic import BaseModel, Field


class WarehouseResponse(BaseModel):
    """Схема для получения информации о складах."""

    wh: int = Field(..., ge=0)


class SizeWarehouseResponse(BaseModel):
    """Схема для получения информации о связи размера и склада."""

    wh: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class SizeResponse(BaseModel):
    """Схема для получения информации о размерах."""

    size: str
    quantity_by_wh: list[SizeWarehouseResponse]


class ProductResponse(BaseModel):
    """Схема для получения информации о товаре."""

    nm_id: int = Field(..., ge=0)
    current_price: int = Field(..., ge=0)
    sum_quantity: int = Field(..., ge=0)

    quantity_by_sizes: list[SizeResponse]


