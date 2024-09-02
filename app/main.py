import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from alembic import command
from alembic.config import Config
from app.api.endpoints import router
from app.core.config import settings


async def run_migrations():
    """Асинхронный запуск миграций Alembic."""
    loop = asyncio.get_event_loop()
    alembic_cfg = Config("alembic.ini")
    await loop.run_in_executor(None, command.upgrade, alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запуск применения миграций при старте приложения."""
    await run_migrations()
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.include_router(router, prefix="/product")
