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


def test_weakness_stats_support_repeat_study_flow() -> None:
    payload = StatsService().get_weakness_stats()

    assert set(payload.model_dump()) == {"weakUnits", "weakQuestions", "weakKeywords"}
