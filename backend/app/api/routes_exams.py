from fastapi import APIRouter, HTTPException

from app.schemas.exam import ExamCreateRequest, ExamDetail, ExamSubmissionRequest
from app.schemas.grading import GradingResult
from app.services.exam_service import ExamService

router = APIRouter(tags=["exams"])


@router.post("/exams", response_model=ExamDetail)
def create_exam(payload: ExamCreateRequest) -> ExamDetail:
    return ExamService().create_exam(payload)


@router.get("/exams/{exam_id}", response_model=ExamDetail)
def get_exam(exam_id: str) -> ExamDetail:
    exam = ExamService().get_exam(exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.post("/exams/{exam_id}/submit", response_model=GradingResult)
def submit_exam(exam_id: str, payload: ExamSubmissionRequest) -> GradingResult:
    result = ExamService().submit_exam(exam_id=exam_id, payload=payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return result


@router.get("/exams/{exam_id}/result", response_model=GradingResult)
def get_exam_result(exam_id: str) -> GradingResult:
    result = ExamService().get_result(exam_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Exam result not found")
    return result
