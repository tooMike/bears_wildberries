from pydantic import BaseModel, Field


class WarehouseBase(BaseModel):
    """Базовая схема склада."""

    wh: int = Field(..., ge=0)
