from pydantic import BaseModel, Field


class SizeBase(BaseModel):
    """Базовая схема размеров."""

    size: str
    product_id: int


class SizeRead(SizeBase):
    """Получение информации о размере"""