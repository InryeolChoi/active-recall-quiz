from app.schemas.exam import ExamQuestion
from app.services.grading_service import GradingService


def test_short_answer_grading() -> None:
    result = GradingService().grade_question(
        ExamQuestion(
            questionId="unit_1_1:part1:1",
            unitId="unit_1_1",
            part="part1",
            type="short_answer",
            prompts=["sample"],
            answersSnapshot=["소프트웨어 생명 주기"],
            aliasesSnapshot=[],
            keywordsSnapshot=["소프트웨어 생명 주기"],
            maxScore=10,
        ),
        "소프트웨어 생명 주기",
    )
    assert result.isCorrect is True
    assert result.earnedScore == 10
