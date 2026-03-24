from pathlib import Path

import pytest

from app.core.config import settings
from app.schemas.content_sync import ContentBundleImportRequest, ContentManifest, SourceDocumentRecord
from app.services.content_sync_service import ContentSyncService
from app.services.question_service import QuestionService, reset_question_cache
from app.services.stats_service import StatsService


def _sample_bundle() -> ContentBundleImportRequest:
    return ContentBundleImportRequest(
        manifest=ContentManifest(
            bundleVersion="bundle-api-contract-001",
            sourceCommit="api-contract-commit",
            generatedAt="2026-03-24T01:00:00+09:00",
            contentHash="sha256:api-contract",
        ),
        documents=[
            SourceDocumentRecord(
                documentId="doc-api-1",
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
            }
        ],
    )


@pytest.fixture()
def imported_runtime_snapshot(tmp_path: Path) -> None:
    original_path = settings.sqlite_path
    settings.sqlite_path = tmp_path / "content.db"
    reset_question_cache()
    ContentSyncService().import_bundle(_sample_bundle())
    yield
    reset_question_cache()
    settings.sqlite_path = original_path


def test_question_detail_hides_answers_by_default(imported_runtime_snapshot: None) -> None:
    question = QuestionService().list_questions(limit=1)[0]

    hidden = QuestionService().get_question(question.questionId)

    assert hidden.questionId == question.questionId
    assert hidden.answers == []
    assert hidden.aliases == []
    assert hidden.keywords == []


def test_question_detail_can_include_answers_for_memorization_helpers(imported_runtime_snapshot: None) -> None:
    question = QuestionService().list_questions(limit=1)[0]

    shown = QuestionService().get_question(question.questionId, include_answer=True)

    assert shown.questionId == question.questionId
    assert shown.answers
    assert shown.keywords


def test_question_list_supports_unit_and_part_filters_for_study_mode(imported_runtime_snapshot: None) -> None:
    service = QuestionService()
    question = service.list_questions(limit=1)[0]

    filtered_by_unit = service.list_questions(unit_id=question.unitId)
    filtered_by_part = service.list_questions(part=question.part)
    filtered_by_both = service.list_questions(unit_id=question.unitId, part=question.part)

    assert filtered_by_unit
    assert all(item.unitId == question.unitId for item in filtered_by_unit)
    assert filtered_by_part
    assert all(item.part == question.part for item in filtered_by_part)
    assert filtered_by_both
    assert all(item.unitId == question.unitId and item.part == question.part for item in filtered_by_both)


def test_unit_summaries_expose_parts_for_study_mode_navigation(imported_runtime_snapshot: None) -> None:
    summaries = QuestionService().list_units()

    assert summaries
    assert all(summary.parts for summary in summaries)
    assert all(summary.questionCount > 0 for summary in summaries)


def test_weakness_stats_support_repeat_study_flow() -> None:
    payload = StatsService().get_weakness_stats()

    assert set(payload.model_dump()) == {"weakUnits", "weakQuestions", "weakKeywords"}
