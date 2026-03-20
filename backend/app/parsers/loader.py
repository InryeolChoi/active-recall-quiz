from pathlib import Path

from app.core.config import settings


def iter_markdown_files() -> list[Path]:
    return sorted(settings.app_root.glob(settings.content_glob))
