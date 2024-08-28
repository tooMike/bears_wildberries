from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = ("Приложение для получение информации о товарах с "
                      "wildberries")
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "MySecretWord"
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
