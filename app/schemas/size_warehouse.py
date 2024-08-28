from pydantic import BaseModel, Field


class SizeWarehouse(BaseModel):
    """Базовая схема для связи размера и склада."""

    size_id: int = Field(..., ge=0)
    warehouse_id: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
