from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://omniroute_app:omniroute@localhost:5432/omniroute"
    database_url_sync: str = "postgresql://omniroute:omniroute@localhost:5432/omniroute"
    openfga_api_url: str = "http://localhost:8080"
    openfga_store_id: str = ""
    openfga_model_id: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    extraction_provider: str = "mock"
    extraction_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    extraction_llm_guard: bool = False
    extraction_parser: str = "stub"
    jwt_secret: str = ""
    jwt_expire_minutes: int = 60
    jwt_refresh_expire_days: int = 14


settings = Settings()
