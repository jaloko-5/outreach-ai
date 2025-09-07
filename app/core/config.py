import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Mystrika-like Email Automation API"
    environment: str = os.getenv("ENVIRONMENT", "dev")

    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:////workspace/app.db"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")

    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_redirect_uri: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:8080/api/auth/google/callback"
    )

    allowed_origins: List[str] = (
        os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv(override=False)
    return Settings()