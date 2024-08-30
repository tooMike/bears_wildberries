from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = ("Приложение для получение информации о товарах с "
                      "wildberries")
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "MySecretWord"
    wildberries_url: str
    celery_broker: str
    celery_backend: str
    pause_between_updates: int = 5
    sleep_between_requests: float = 1
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
