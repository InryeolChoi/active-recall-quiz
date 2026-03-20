from fastapi import APIRouter, Query

from app.schemas.question import QuestionDetail
from app.services.question_service import QuestionService

router = APIRouter(tags=["questions"])


@router.get("/questions", response_model=list[QuestionDetail])
def list_questions(
    unit_id: str | None = Query(default=None, alias="unitId"),
    part: str | None = None,
    type_: str | None = Query(default=None, alias="type"),
    limit: int | None = Query(default=None, ge=1, le=200),
) -> list[QuestionDetail]:
    return QuestionService().list_questions(
        unit_id=unit_id,
        part=part,
        type_=type_,
        limit=limit,
    )


@router.get("/questions/{question_id}", response_model=QuestionDetail)
def get_question(
    question_id: str,
    include_answer: bool = Query(default=False, alias="includeAnswer"),
) -> QuestionDetail:
    return QuestionService().get_question(question_id=question_id, include_answer=include_answer)
