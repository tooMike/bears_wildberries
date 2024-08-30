import httpx
from fastapi import HTTPException

from app.core.config import settings


async def get_product_info(nm_id: int):
    """Получение информации о товаре с Wildberries."""

    url = f"{settings.wildberries_url}{nm_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Товар не найден")

    data = response.json()

    # Проверяем, есть ли нужные данные в ответе
    if not data.get("data", {}).get("products"):
        raise HTTPException(status_code=404, detail="Товар не найден")

    # Предполагаем, что всегда есть хотя бы один продукт
    product_data = data["data"]["products"][0]

    return product_data
