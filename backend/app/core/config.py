from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://omniroute:omniroute@localhost:5432/omniroute"
    database_url_sync: str = "postgresql://omniroute:omniroute@localhost:5432/omniroute"


settings = Settings()
