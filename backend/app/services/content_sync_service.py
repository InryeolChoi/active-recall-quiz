from app.repositories.content_store import ContentStore
from app.schemas.content_sync import ContentBundleImportRequest, ContentBundleImportResult
from app.services.question_service import reset_question_cache


class ContentSyncService:
    def import_bundle(self, payload: ContentBundleImportRequest) -> ContentBundleImportResult:
        result = ContentStore().import_bundle(payload)
        reset_question_cache()
        return result
