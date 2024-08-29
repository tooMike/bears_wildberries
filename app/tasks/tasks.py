import asyncio

from app.celery import celery_app
from app.crud.product import product_crud


@celery_app.task
def update_products():
    async def inner():
        products = await product_crud.get_multi()
        for product in products:

    loop = asyncio.new_event_loop()
    loop.run_until_complete(inner())