from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
)

# Настройки периодических задач
celery_app.conf.beat_schedule = {
    'update-products-every-5-minutes': {
        'task': 'app.tasks.update_products',
        'schedule': crontab(minute='*/5'),  # Каждые 5 минут
    },
}

celery_app.conf.timezone = 'UTC'

celery_app.autodiscover_tasks(['app.api', 'tasks'])
