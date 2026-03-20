from collections import defaultdict
from datetime import datetime
import random
from zoneinfo import ZoneInfo

from app.schemas.exam import (
    ExamCreateRequest,
    ExamDetail,
    ExamQuestion,
    ExamSubmissionRequest,
)
from app.schemas.grading import GradingResult
from app.services.grading_service import GradingService
from app.services.question_service import QuestionService

SEOUL = ZoneInfo("Asia/Seoul")
_exam_store: dict[str, ExamDetail] = {}
_result_store: dict[str, GradingResult] = {}
_exam_counter = defaultdict(int)


class ExamService:
    def create_exam(self, payload: ExamCreateRequest) -> ExamDetail:
        questions = QuestionService().list_questions(
            unit_id=payload.unitIds[0] if len(payload.unitIds) == 1 else None,
            part=payload.parts[0] if len(payload.parts) == 1 else None,
        )
        if payload.unitIds:
            questions = [question for question in questions if question.unitId in payload.unitIds]
        if payload.parts:
            questions = [question for question in questions if question.part in payload.parts]
        if payload.shuffle:
            random.shuffle(questions)
        if payload.questionCount:
            questions = questions[: payload.questionCount]

        now = datetime.now(SEOUL)
        counter_key = now.strftime("%Y%m%d")
        _exam_counter[counter_key] += 1
        exam_id = f"exam_{counter_key}_{_exam_counter[counter_key]:03d}"

        exam_questions = [
            ExamQuestion(
                questionId=question.questionId,
                unitId=question.unitId,
                part=question.part,
                type=question.type,
                prompts=question.prompts,
                answersSnapshot=question.answers,
                aliasesSnapshot=question.aliases,
                keywordsSnapshot=question.keywords,
                maxScore=10,
            )
            for question in questions
        ]
        exam = ExamDetail(
            examId=exam_id,
            mode=payload.mode,
            createdAt=now.isoformat(),
            unitIds=payload.unitIds,
            parts=payload.parts,
            questionCount=len(exam_questions),
            questions=exam_questions,
        )
        _exam_store[exam_id] = exam
        return exam

    def get_exam(self, exam_id: str) -> ExamDetail | None:
        return _exam_store.get(exam_id)

    def submit_exam(self, exam_id: str, payload: ExamSubmissionRequest) -> GradingResult | None:
        exam = _exam_store.get(exam_id)
        if exam is None:
            return None

        answer_map = {answer.questionId: answer.responseText for answer in payload.answers}
        grader = GradingService()
        question_results = [
            grader.grade_question(question, answer_map.get(question.questionId, ""))
            for question in exam.questions
        ]
        score = sum(result.earnedScore for result in question_results)
        total = sum(result.maxScore for result in question_results)
        grading_result = GradingResult(
            examId=exam_id,
            score=score,
            total=total,
            submittedAt=datetime.now(SEOUL).isoformat(),
            results=question_results,
        )
        _result_store[exam_id] = grading_result
        return grading_result

    def get_result(self, exam_id: str) -> GradingResult | None:
        return _result_store.get(exam_id)
