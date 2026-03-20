from typing import Literal

from pydantic import BaseModel, Field

QuestionType = Literal["short_answer", "list_answer"]


class UnitSummary(BaseModel):
    unitId: str
    title: str
    parts: list[str]
    questionCount: int


class QuestionDetail(BaseModel):
    questionId: str
    unitId: str
    part: str
    title: str | None = None
    type: QuestionType
    prompts: list[str]
    answers: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    sourcePath: str
    sourceLine: int
