import asyncio

from app.api.background_tasks import save_or_update_product
from app.api.utils import get_product_info
from app.celery import celery_app
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud.product import product_crud


@celery_app.task
def update_products():
    """Обновление информации о всех продуктах, сохраненных в БД."""
    async def inner():
        async with AsyncSessionLocal() as session:
            products = await product_crud.get_multi(session)
            for product in products:
                product_data = await get_product_info(product.nm_id)
                await save_or_update_product(product_data, session)
                # Добавляем паузу между запросами
                await asyncio.sleep(settings.sleep_between_requests)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(inner())
