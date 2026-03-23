from app.services.question_service import QuestionService
from app.services.stats_service import StatsService


def test_question_detail_hides_answers_by_default() -> None:
    question = QuestionService().list_questions(limit=1)[0]

    hidden = QuestionService().get_question(question.questionId)

    assert hidden.questionId == question.questionId
    assert hidden.answers == []
    assert hidden.aliases == []
    assert hidden.keywords == []


def test_question_detail_can_include_answers_for_memorization_helpers() -> None:
    question = QuestionService().list_questions(limit=1)[0]

    shown = QuestionService().get_question(question.questionId, include_answer=True)

    assert shown.questionId == question.questionId
    assert shown.answers
    assert shown.keywords


def test_question_list_supports_unit_and_part_filters_for_study_mode() -> None:
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


def test_unit_summaries_expose_parts_for_study_mode_navigation() -> None:
    summaries = QuestionService().list_units()

    assert summaries
    assert all(summary.parts for summary in summaries)
    assert all(summary.questionCount > 0 for summary in summaries)


def test_weakness_stats_support_repeat_study_flow() -> None:
    payload = StatsService().get_weakness_stats()

    assert set(payload.model_dump()) == {"weakUnits", "weakQuestions", "weakKeywords"}
