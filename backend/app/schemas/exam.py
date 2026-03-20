from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.question import QuestionType

ExamMode = Literal["study", "exam"]


class ExamCreateRequest(BaseModel):
    unitIds: list[str] = Field(default_factory=list)
    parts: list[str] = Field(default_factory=list)
    questionCount: int = Field(default=10, ge=1, le=100)
    mode: ExamMode = "exam"
    shuffle: bool = False


class ExamQuestion(BaseModel):
    questionId: str
    unitId: str
    part: str
    type: QuestionType
    prompts: list[str]
    answersSnapshot: list[str]
    aliasesSnapshot: list[str] = Field(default_factory=list)
    keywordsSnapshot: list[str] = Field(default_factory=list)
    maxScore: int = 10


class ExamDetail(BaseModel):
    examId: str
    mode: ExamMode
    createdAt: str
    unitIds: list[str]
    parts: list[str]
    questionCount: int
    questions: list[ExamQuestion]


class SubmittedAnswer(BaseModel):
    questionId: str
    responseText: str


class ExamSubmissionRequest(BaseModel):
    answers: list[SubmittedAnswer]
