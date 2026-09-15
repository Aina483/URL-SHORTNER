
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    base_url: str = "http://localhost:8000"
    database_url: str = "sqlite+aiosqlite:///./shortener.db"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    short_code_length: int = 7
    max_code_generation_attempts: int = 5
    rate_limit: str = "20/minute"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is only parsed once per process."""
    return Settings()


settings = get_settings()
