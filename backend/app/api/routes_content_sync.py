from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from app.core.config import settings
from app.schemas.content_sync import ContentBundleImportRequest, ContentBundleImportResult
from app.services.content_sync_service import ContentSyncService

router = APIRouter(tags=["content-sync"])


@router.post("/content-sync/bundles", response_model=ContentBundleImportResult)
def import_content_bundle(
    payload: ContentBundleImportRequest,
    content_sync_token: Annotated[str | None, Header(alias="X-Content-Sync-Token")] = None,
) -> ContentBundleImportResult:
    if not settings.content_sync_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Content sync token is not configured.",
        )

    if content_sync_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing content sync token.",
        )

    if content_sync_token != settings.content_sync_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid content sync token.",
        )

    return ContentSyncService().import_bundle(payload)
