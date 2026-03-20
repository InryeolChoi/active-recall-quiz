from fastapi import APIRouter

from app.schemas.grading import WeaknessStats
from app.services.stats_service import StatsService

router = APIRouter(tags=["stats"])


@router.get("/stats/weakness", response_model=WeaknessStats)
def get_weakness_stats() -> WeaknessStats:
    return StatsService().get_weakness_stats()
