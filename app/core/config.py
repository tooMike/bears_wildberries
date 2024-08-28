from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = ("Приложение для получение информации о товарах с "
                      "wildberries")
    database_url: str = "postgresql+asyncpg://user:password@db/dbname"
    secret: str = "Секретное слово"
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
