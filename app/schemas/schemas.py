from pydantic import BaseModel, ConfigDict, Field


class WarehouseResponse(BaseModel):
    """Схема для получения информации о складах."""

    wh: int = Field(..., ge=0)
    model_config = ConfigDict(from_attributes=True)


class SizeWarehouseResponse(BaseModel):
    """Схема для получения информации о связи размера и склада."""

    wh: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    model_config = ConfigDict(from_attributes=True)


class SizeResponse(BaseModel):
    """Схема для получения информации о размерах."""

    size: str
    quantity_by_wh: list[SizeWarehouseResponse]
    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    """Схема для получения информации о товаре."""

    nm_id: int = Field(..., ge=0)
    current_price: int = Field(..., ge=0)
    sum_quantity: int = Field(..., ge=0)
    quantity_by_sizes: list[SizeResponse]
    model_config = ConfigDict(from_attributes=True)
