from functools import lru_cache

from fastapi import HTTPException

from app.repositories.content_store import ContentStore
from app.schemas.question import QuestionDetail, UnitSummary


@lru_cache(maxsize=1)
def _load_questions() -> list[QuestionDetail]:
    return ContentStore().list_active_questions()


def reset_question_cache() -> None:
    _load_questions.cache_clear()


class QuestionService:
    def list_units(self) -> list[UnitSummary]:
        grouped: dict[str, list[QuestionDetail]] = {}
        for question in _load_questions():
            grouped.setdefault(question.unitId, []).append(question)

        summaries: list[UnitSummary] = []
        for unit_id, questions in grouped.items():
            parts = sorted({question.part for question in questions})
            summaries.append(
                UnitSummary(
                    unitId=unit_id,
                    title=unit_id,
                    parts=parts,
                    questionCount=len(questions),
                )
            )
        return summaries

    def list_questions(
        self,
        unit_id: str | None = None,
        part: str | None = None,
        type_: str | None = None,
        limit: int | None = None,
    ) -> list[QuestionDetail]:
        questions = _load_questions()
        if unit_id:
            questions = [question for question in questions if question.unitId == unit_id]
        if part:
            questions = [question for question in questions if question.part == part]
        if type_:
            questions = [question for question in questions if question.type == type_]
        if limit is not None:
            questions = questions[:limit]
        return questions

    def get_question(self, question_id: str, include_answer: bool = False) -> QuestionDetail:
        for question in _load_questions():
            if question.questionId == question_id:
                if include_answer:
                    return question
                return question.model_copy(update={"answers": [], "aliases": [], "keywords": []})
        raise HTTPException(status_code=404, detail="Question not found")
