import os
from pathlib import Path

from pydantic import BaseModel, Field


def _default_sqlite_path() -> Path:
    app_root = Path(__file__).resolve().parents[3]
    return Path(os.getenv("SQLITE_PATH", str(app_root / "backend" / "data" / "content.db")))


class Settings(BaseModel):
    app_root: Path = Path(__file__).resolve().parents[3]
    sqlite_path: Path = Field(default_factory=_default_sqlite_path)
    content_sync_token: str | None = os.getenv("CONTENT_SYNC_TOKEN")


settings = Settings()
