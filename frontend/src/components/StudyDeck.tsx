"use client";

import { useState } from "react";

import { QuestionCard } from "@/components/QuestionCard";
import type { QuestionDetail } from "@/lib/types";

type Props = {
  questions: QuestionDetail[];
};

export function StudyDeck({ questions }: Props) {
  const [revealedIds, setRevealedIds] = useState<Record<string, boolean>>({});
  const [rememberedIds, setRememberedIds] = useState<Record<string, boolean>>({});
  const [hideRemembered, setHideRemembered] = useState(true);

  const rememberedCount = questions.filter((question) => rememberedIds[question.questionId]).length;
  const remainingCount = questions.length - rememberedCount;
  const visibleQuestions = hideRemembered
    ? questions.filter((question) => !rememberedIds[question.questionId])
    : questions;

  function toggleAnswer(questionId: string) {
    setRevealedIds((current) => ({
      ...current,
      [questionId]: !current[questionId]
    }));
  }

  function toggleRemembered(questionId: string) {
    setRememberedIds((current) => ({
      ...current,
      [questionId]: !current[questionId]
    }));
  }

  function resetSession() {
    setRevealedIds({});
    setRememberedIds({});
    setHideRemembered(true);
  }

  return (
    <div className="stack">
      <section className="panel stack">
        <div className="actions">
          <div className="badge">전체 {questions.length}</div>
          <div className="badge secondary-badge">외운 문제 {rememberedCount}</div>
          <div className="badge secondary-badge">다시 볼 문제 {remainingCount}</div>
        </div>
        <label className="checkbox-row">
          <input
            checked={hideRemembered}
            type="checkbox"
            onChange={(event) => setHideRemembered(event.target.checked)}
          />
          <span>외운 문제는 목록에서 숨기기</span>
        </label>
        <div className="actions">
          <button className="secondary" type="button" onClick={resetSession}>
            다시 시작하기
          </button>
        </div>
      </section>

      {visibleQuestions.length === 0 ? (
        <section className="panel stack">
          <h2>모든 문제를 외웠습니다.</h2>
          <p className="muted">외운 문제 숨기기를 끄면 다시 전체 목록을 볼 수 있습니다.</p>
        </section>
      ) : null}

      {visibleQuestions.map((question, index) => {
        const isRevealed = revealedIds[question.questionId] ?? false;
        const isRemembered = rememberedIds[question.questionId] ?? false;

        return (
          <QuestionCard
            key={question.questionId}
            index={index}
            prompts={question.prompts}
            meta={`${question.unitId} / ${question.part} / ${question.type}`}
          >
            <div className="stack">
              {isRevealed ? (
                <div className="study-answer">
                  <strong>정답</strong>
                  <p>{question.answers.join(" / ")}</p>
                </div>
              ) : (
                <p className="muted">답을 먼저 떠올려 보고, 필요할 때만 정답을 확인하세요.</p>
              )}
              <div className="actions">
                <button className="secondary" type="button" onClick={() => toggleAnswer(question.questionId)}>
                  {isRevealed ? "정답 숨기기" : "정답 보기"}
                </button>
                <button
                  type="button"
                  className={isRemembered ? "secondary" : undefined}
                  onClick={() => toggleRemembered(question.questionId)}
                >
                  {isRemembered ? "다시 볼래요" : "외웠어요"}
                </button>
              </div>
            </div>
          </QuestionCard>
        );
      })}
    </div>
  );
}
