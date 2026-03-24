import os
from pathlib import Path

from pydantic import BaseModel, Field


def _default_sqlite_path() -> Path:
    app_root = Path(__file__).resolve().parents[3]
    return Path(os.getenv("SQLITE_PATH", str(app_root / "backend" / "data" / "content.db")))


def _default_content_sync_token() -> str | None:
    return os.getenv("CONTENT_SYNC_TOKEN")


def _default_content_sync_rate_limit_max_requests() -> int:
    return int(os.getenv("CONTENT_SYNC_RATE_LIMIT_MAX_REQUESTS", "10"))


def _default_content_sync_rate_limit_window_seconds() -> int:
    return int(os.getenv("CONTENT_SYNC_RATE_LIMIT_WINDOW_SECONDS", "60"))


class Settings(BaseModel):
    app_root: Path = Path(__file__).resolve().parents[3]
    sqlite_path: Path = Field(default_factory=_default_sqlite_path)
    content_sync_token: str | None = Field(default_factory=_default_content_sync_token)
    content_sync_rate_limit_max_requests: int = Field(default_factory=_default_content_sync_rate_limit_max_requests)
    content_sync_rate_limit_window_seconds: int = Field(default_factory=_default_content_sync_rate_limit_window_seconds)


settings = Settings()
