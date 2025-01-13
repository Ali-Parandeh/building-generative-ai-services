# settings.py

from typing import Annotated
from pydantic import Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    port: Annotated[int, Field(default=8000)]
    app_secret: Annotated[str, Field(min_length=32)]
    pg_dsn: Annotated[
        PostgresDsn,
        Field(
            alias="DATABASE_URL",
            default="postgres://user:pass@localhost:5432/database",
        ),
    ]
    cors_whitelist_domains: Annotated[
        set[HttpUrl],
        Field(alias="CORS_WHITELIST", default=["http://localhost:3000"]),
    ]


settings = AppSettings()
