from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_root: Path = Path(__file__).resolve().parents[3]
    content_glob: str = "unit_*/*.md"
    sqlite_path: Path = app_root / "backend" / "data" / "content.db"


settings = Settings()
