from fastapi import APIRouter

from app.schemas.content_sync import ContentBundleImportRequest, ContentBundleImportResult
from app.services.content_sync_service import ContentSyncService

router = APIRouter(tags=["content-sync"])


@router.post("/content-sync/bundles", response_model=ContentBundleImportResult)
def import_content_bundle(payload: ContentBundleImportRequest) -> ContentBundleImportResult:
    return ContentSyncService().import_bundle(payload)
