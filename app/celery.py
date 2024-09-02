from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "app",
    broker=settings.celery_broker,
    backend=settings.celery_backend
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
)

# Настройки периодических задач (обновление данные в БД о товарах)
celery_app.conf.beat_schedule = {
    "update-products-every-x-minutes": {
        "task": "app.tasks.tasks.update_products",
        "schedule": crontab(
            minute=f"*/{settings.pause_between_updates}"
        ),
    },
}

celery_app.conf.timezone = "UTC"

celery_app.autodiscover_tasks(["app.tasks"])
