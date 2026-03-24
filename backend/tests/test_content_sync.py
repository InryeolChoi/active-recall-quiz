from pathlib import Path

import pytest
from fastapi import HTTPException

from app.api.routes_content_sync import import_content_bundle
from app.core.config import Settings, settings
from app.schemas.content_sync import (
    ContentBundleImportRequest,
    ContentManifest,
    SourceDocumentRecord,
)
from app.services.content_sync_rate_limiter import content_sync_rate_limiter
from app.services.content_sync_service import ContentSyncService
from app.services.question_service import QuestionService, reset_question_cache


def _sample_bundle(bundle_version: str = "bundle-20260324-001") -> ContentBundleImportRequest:
    return ContentBundleImportRequest(
        manifest=ContentManifest(
            bundleVersion=bundle_version,
            sourceCommit="abc123def456",
            generatedAt="2026-03-24T01:00:00+09:00",
            contentHash="sha256:sample",
        ),
        documents=[
            SourceDocumentRecord(
                documentId="doc-1",
                unitId="unit_sync",
                part="part1",
                title="Imported Unit",
                sourcePath="exports/unit_sync/part1.md",
            )
        ],
        questions=[
            {
                "questionId": "unit_sync:part1:1",
                "unitId": "unit_sync",
                "part": "part1",
                "title": "Imported Unit",
                "type": "short_answer",
                "prompts": ["외부 노트 적재 경로를 설명하시오."],
                "answers": ["SQLite 적재 파이프라인"],
                "aliases": [],
                "keywords": ["SQLite 적재 파이프라인"],
                "warnings": [],
                "sourcePath": "exports/unit_sync/part1.md",
                "sourceLine": 3,
            },
            {
                "questionId": "unit_sync:part1:2",
                "unitId": "unit_sync",
                "part": "part1",
                "title": "Imported Unit",
                "type": "list_answer",
                "prompts": ["번들 계약에 포함될 항목을 쓰시오."],
                "answers": ["manifest.json", "question records"],
                "aliases": [],
                "keywords": ["manifest.json", "question records"],
                "warnings": [],
                "sourcePath": "exports/unit_sync/part1.md",
                "sourceLine": 8,
            },
        ],
    )


@pytest.fixture()
def isolated_sqlite(tmp_path: Path) -> None:
    original_path = settings.sqlite_path
    settings.sqlite_path = tmp_path / "content.db"
    reset_question_cache()
    content_sync_rate_limiter.reset()
    yield
    content_sync_rate_limiter.reset()
    reset_question_cache()
    settings.sqlite_path = original_path


def test_imported_bundle_becomes_runtime_source(isolated_sqlite: None) -> None:
    result = ContentSyncService().import_bundle(_sample_bundle())

    questions = QuestionService().list_questions()
    summaries = QuestionService().list_units()

    assert result.importedQuestionCount == 2
    assert len(questions) == 2
    assert questions[0].sourcePath == "exports/unit_sync/part1.md"
    assert [summary.unitId for summary in summaries] == ["unit_sync"]
    assert summaries[0].questionCount == 2


def test_runtime_lists_are_empty_without_active_snapshot(isolated_sqlite: None) -> None:
    assert QuestionService().list_questions() == []
    assert QuestionService().list_units() == []


def test_import_creates_sqlite_file(isolated_sqlite: None) -> None:
    sqlite_path = settings.sqlite_path

    assert not sqlite_path.exists()

    ContentSyncService().import_bundle(_sample_bundle())

    assert sqlite_path.exists()


def test_import_reuses_existing_snapshot_for_same_bundle_version(isolated_sqlite: None) -> None:
    first = ContentSyncService().import_bundle(_sample_bundle())
    second = ContentSyncService().import_bundle(_sample_bundle())

    questions = QuestionService().list_questions()

    assert first.reusedSnapshot is False
    assert second.reusedSnapshot is True
    assert second.snapshotId == first.snapshotId
    assert len(questions) == 2


@pytest.fixture()
def content_sync_token() -> None:
    original_token = settings.content_sync_token
    settings.content_sync_token = "test-sync-token"
    original_max_requests = settings.content_sync_rate_limit_max_requests
    original_window_seconds = settings.content_sync_rate_limit_window_seconds
    settings.content_sync_rate_limit_max_requests = 10
    settings.content_sync_rate_limit_window_seconds = 60
    yield
    settings.content_sync_token = original_token
    settings.content_sync_rate_limit_max_requests = original_max_requests
    settings.content_sync_rate_limit_window_seconds = original_window_seconds


def test_content_sync_requires_token(isolated_sqlite: None, content_sync_token: None) -> None:
    with pytest.raises(HTTPException) as exc_info:
        import_content_bundle(_sample_bundle())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Missing content sync token."


def test_content_sync_rejects_invalid_token(isolated_sqlite: None, content_sync_token: None) -> None:
    with pytest.raises(HTTPException) as exc_info:
        import_content_bundle(_sample_bundle(), content_sync_token="wrong-token")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid content sync token."


def test_content_sync_accepts_valid_token(isolated_sqlite: None, content_sync_token: None) -> None:
    response = import_content_bundle(_sample_bundle(), content_sync_token="test-sync-token")

    assert response.importedQuestionCount == 2


def test_content_sync_returns_503_when_server_token_is_unset(isolated_sqlite: None) -> None:
    original_token = settings.content_sync_token
    settings.content_sync_token = None

    try:
        with pytest.raises(HTTPException) as exc_info:
            import_content_bundle(_sample_bundle(), content_sync_token="any-token")
    finally:
        settings.content_sync_token = original_token

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Content sync token is not configured."


def test_content_sync_rate_limit_allows_requests_within_window(
    isolated_sqlite: None, content_sync_token: None
) -> None:
    settings.content_sync_rate_limit_max_requests = 2
    settings.content_sync_rate_limit_window_seconds = 60

    assert content_sync_rate_limiter.allow("test-sync-token", now=0.0) is True
    assert content_sync_rate_limiter.allow("test-sync-token", now=10.0) is True


def test_content_sync_rate_limit_rejects_excess_requests(
    isolated_sqlite: None, content_sync_token: None
) -> None:
    settings.content_sync_rate_limit_max_requests = 2
    settings.content_sync_rate_limit_window_seconds = 60
    content_sync_rate_limiter.reset()

    import_content_bundle(_sample_bundle("bundle-20260324-003"), content_sync_token="test-sync-token")
    import_content_bundle(_sample_bundle("bundle-20260324-004"), content_sync_token="test-sync-token")

    with pytest.raises(HTTPException) as exc_info:
        import_content_bundle(_sample_bundle("bundle-20260324-005"), content_sync_token="test-sync-token")

    assert exc_info.value.status_code == 429
    assert exc_info.value.detail == "Content sync rate limit exceeded."


def test_content_sync_rate_limit_window_expires(
    isolated_sqlite: None, content_sync_token: None
) -> None:
    settings.content_sync_rate_limit_max_requests = 2
    settings.content_sync_rate_limit_window_seconds = 60
    content_sync_rate_limiter.reset()

    assert content_sync_rate_limiter.allow("test-sync-token", now=0.0) is True
    assert content_sync_rate_limiter.allow("test-sync-token", now=10.0) is True
    assert content_sync_rate_limiter.allow("test-sync-token", now=61.0) is True


def test_settings_reads_sqlite_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_path = "/data/content.db"
    monkeypatch.setenv("SQLITE_PATH", expected_path)

    configured = Settings()

    assert configured.sqlite_path == Path(expected_path)


def test_settings_reads_content_sync_rate_limit_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CONTENT_SYNC_RATE_LIMIT_MAX_REQUESTS", "15")
    monkeypatch.setenv("CONTENT_SYNC_RATE_LIMIT_WINDOW_SECONDS", "120")

    configured = Settings()

    assert configured.content_sync_rate_limit_max_requests == 15
    assert configured.content_sync_rate_limit_window_seconds == 120
