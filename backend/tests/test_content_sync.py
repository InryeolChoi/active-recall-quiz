from pathlib import Path

import pytest

from app.core.config import settings
from app.schemas.content_sync import (
    ContentBundleImportRequest,
    ContentManifest,
    SourceDocumentRecord,
)
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
    yield
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


def test_import_reuses_existing_snapshot_for_same_bundle_version(isolated_sqlite: None) -> None:
    first = ContentSyncService().import_bundle(_sample_bundle())
    second = ContentSyncService().import_bundle(_sample_bundle())

    questions = QuestionService().list_questions()

    assert first.reusedSnapshot is False
    assert second.reusedSnapshot is True
    assert second.snapshotId == first.snapshotId
    assert len(questions) == 2
