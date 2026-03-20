from fastapi import APIRouter

from app.schemas.question import UnitSummary
from app.services.question_service import QuestionService

router = APIRouter(tags=["units"])


@router.get("/units", response_model=list[UnitSummary])
def list_units() -> list[UnitSummary]:
    return QuestionService().list_units()
