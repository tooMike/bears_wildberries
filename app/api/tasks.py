import asyncio

from app.api.background_tasks import save_or_update_product
from app.celery import celery_app
from app.core.db import AsyncSessionLocal


@celery_app.task
def save_product_async_task(product_data_):
    """Сохранение информации о товаре в БД (с асинхронной реализацией)."""

    async def inner(product_data):
        async with AsyncSessionLocal() as session:
            await save_or_update_product(product_data, session)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(inner(product_data_))
