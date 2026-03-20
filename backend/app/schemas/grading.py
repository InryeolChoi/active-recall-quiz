from pydantic import BaseModel, Field

from app.schemas.question import QuestionType


class QuestionGradingResult(BaseModel):
    questionId: str
    type: QuestionType
    isCorrect: bool
    earnedScore: int
    maxScore: int
    userAnswer: str
    expectedAnswers: list[str]
    matchedKeywords: list[str] = Field(default_factory=list)
    missingKeywords: list[str] = Field(default_factory=list)
    feedback: str


class GradingResult(BaseModel):
    examId: str
    score: int
    total: int
    submittedAt: str
    results: list[QuestionGradingResult]


class WeaknessPoint(BaseModel):
    name: str
    value: int


class WeaknessStats(BaseModel):
    weakUnits: list[WeaknessPoint] = Field(default_factory=list)
    weakQuestions: list[WeaknessPoint] = Field(default_factory=list)
    weakKeywords: list[WeaknessPoint] = Field(default_factory=list)
