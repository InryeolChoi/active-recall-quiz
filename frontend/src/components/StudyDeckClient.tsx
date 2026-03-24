"use client";

import { useEffect, useMemo, useState } from "react";

import { QuestionCard } from "@/components/QuestionCard";
import type { QuestionDetail, UnitSummary } from "@/lib/types";

type Props = {
  questions: QuestionDetail[];
  units: UnitSummary[];
};

type Direction = "forward" | "backward";

function shorten(text: string, maxLength = 56) {
  if (text.length <= maxLength) {
    return text;
  }

  return `${text.slice(0, maxLength - 1).trimEnd()}…`;
}

function getQuestionLabel(question: QuestionDetail) {
  return question.title?.trim() || question.prompts[0] || question.questionId;
}

export function StudyDeckClient({ questions, units }: Props) {
  const [selectedUnitId, setSelectedUnitId] = useState("");
  const [selectedPart, setSelectedPart] = useState("");
  const [hideRemembered, setHideRemembered] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [rememberedIds, setRememberedIds] = useState<Record<string, boolean>>({});
  const [revealAnswer, setRevealAnswer] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [direction, setDirection] = useState<Direction>("forward");
  const [menuCollapsed, setMenuCollapsed] = useState(false);
  const [cardsVisible, setCardsVisible] = useState(false);

  const selectedUnit = units.find((unit) => unit.unitId === selectedUnitId) ?? null;
  const partOptions = selectedUnit?.parts ?? [];
  const isScopeReady = selectedUnitId !== "" && selectedPart !== "";

  const catalogQuestions = useMemo(
    () =>
      questions.filter((question) => {
        if (!isScopeReady) {
          return false;
        }

        return question.unitId === selectedUnitId && question.part === selectedPart;
      }),
    [isScopeReady, questions, selectedPart, selectedUnitId]
  );

  const visibleQuestions = useMemo(
    () => (hideRemembered ? catalogQuestions.filter((question) => !rememberedIds[question.questionId]) : catalogQuestions),
    [catalogQuestions, hideRemembered, rememberedIds]
  );

  const visibleCount = visibleQuestions.length;
  const activeIndex = visibleCount === 0 ? 0 : Math.min(currentIndex, visibleCount - 1);
  const currentQuestion = visibleCount > 0 ? visibleQuestions[activeIndex] : null;
  const rememberedCount = catalogQuestions.filter((question) => rememberedIds[question.questionId]).length;
  const progressValue = visibleCount === 0 ? 0 : ((activeIndex + 1) / visibleCount) * 100;

  useEffect(() => {
    setCurrentIndex(0);
    setRevealAnswer(false);
    setShowHint(false);
    setMenuCollapsed(false);
  }, [hideRemembered, selectedPart, selectedUnitId]);

  useEffect(() => {
    if (!selectedUnit) {
      if (selectedPart !== "") {
        setSelectedPart("");
      }
      return;
    }

    if (selectedPart !== "" && !partOptions.includes(selectedPart)) {
      setSelectedPart("");
    }
  }, [partOptions, selectedPart, selectedUnit]);

  useEffect(() => {
    if (!isScopeReady) {
      setCardsVisible(false);
      return;
    }

    setCardsVisible(false);
    const timeout = window.setTimeout(() => setCardsVisible(true), 80);
    return () => window.clearTimeout(timeout);
  }, [isScopeReady, selectedPart, selectedUnitId]);

  function goToIndex(nextIndex: number, nextDirection: Direction) {
    if (visibleCount === 0) {
      return;
    }

    const clampedIndex = Math.max(0, Math.min(nextIndex, visibleCount - 1));
    setDirection(nextDirection);
    setCurrentIndex(clampedIndex);
    setRevealAnswer(false);
    setShowHint(false);
  }

  function handleRemembered(questionId: string, nextRemembered: boolean) {
    setRememberedIds((current) => ({
      ...current,
      [questionId]: nextRemembered
    }));
    setRevealAnswer(false);
    setShowHint(false);

    if (!hideRemembered) {
      goToIndex(activeIndex + 1, "forward");
    }
  }

  function resetSession() {
    setSelectedUnitId("");
    setSelectedPart("");
    setHideRemembered(true);
    setCurrentIndex(0);
    setRememberedIds({});
    setRevealAnswer(false);
    setShowHint(false);
    setDirection("forward");
    setMenuCollapsed(false);
    setCardsVisible(false);
  }

  function handleTocSelect(index: number) {
    goToIndex(index, index > activeIndex ? "forward" : "backward");
    setMenuCollapsed(true);
  }

  return (
    <div className="stack">
      <section className={`panel stack study-toolbar ${menuCollapsed ? "study-toolbar--collapsed" : ""}`}>
        <div className="study-toolbar-head">
          <div className="stack">
            <div className="badge">목차</div>
            <h2>범위를 먼저 고른 뒤, 카드 한 장씩 회상해 보세요.</h2>
            <p className="muted">
              단원과 파트를 정하면 그 범위의 카드만 모아서 보여주고, 원하는 카드를 눌러 바로 학습을 시작할 수 있습니다.
            </p>
          </div>

          <div className="study-badges">
            <div className="badge">전체 {catalogQuestions.length}</div>
            <div className="badge secondary-badge">학습 중 {visibleCount}</div>
            <div className="badge secondary-badge">외운 문제 {rememberedCount}</div>
          </div>
        </div>

        {menuCollapsed ? (
          <div className="study-collapsed-bar">
            <div className="stack">
              <strong>
                {selectedUnit?.unitId ?? "단원 미선택"} / {selectedPart || "파트 미선택"}
              </strong>
              <p className="muted">선택한 범위에서 {catalogQuestions.length}문제를 불러왔습니다.</p>
            </div>
            <div className="actions">
              <button className="secondary" type="button" onClick={() => setMenuCollapsed(false)}>
                목차 다시 열기
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="study-filter-grid">
              <label className="stack">
                <span>단원</span>
                <select value={selectedUnitId} onChange={(event) => setSelectedUnitId(event.target.value)}>
                  <option value="">단원을 먼저 골라주세요</option>
                  {units.map((unit) => (
                    <option key={unit.unitId} value={unit.unitId}>
                      {unit.unitId} · {unit.title}
                    </option>
                  ))}
                </select>
              </label>

              <label className="stack">
                <span>파트</span>
                <select
                  value={selectedPart}
                  disabled={!selectedUnit}
                  onChange={(event) => setSelectedPart(event.target.value)}
                >
                  <option value="">{selectedUnit ? "파트를 골라주세요" : "먼저 단원을 골라주세요"}</option>
                  {partOptions.map((part) => (
                    <option key={part} value={part}>
                      {part}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="study-meta-row">
              <label className="checkbox-row">
                <input
                  checked={hideRemembered}
                  type="checkbox"
                  onChange={(event) => setHideRemembered(event.target.checked)}
                />
                <span>외운 문제는 카드에서 숨기기</span>
              </label>

              <div className="actions">
                <button className="secondary" type="button" onClick={resetSession}>
                  초기화
                </button>
              </div>
            </div>

            <div className="study-progress">
              <div className="study-progress-track" aria-hidden="true">
                <span style={{ width: `${progressValue}%` }} />
              </div>
              <p className="muted">
                {selectedUnit ? `${selectedUnit.unitId} · ${selectedUnit.title}` : "단원을 먼저 선택하세요"} /{" "}
                {selectedPart || "파트를 고르면 카드가 나타납니다"}
              </p>
            </div>

            {!isScopeReady ? (
              <div className="study-empty-state stack">
                <strong>학습 범위를 먼저 골라주세요.</strong>
                <p className="muted">단원과 파트를 모두 선택하면, 그 순간 카드 목록이 애니메이션과 함께 나타납니다.</p>
              </div>
            ) : (
              <div className={`toc-grid toc-grid--animated ${cardsVisible ? "visible" : ""}`} role="list" aria-label="학습 목차">
                {visibleQuestions.length === 0 ? (
                  <p className="muted">선택한 범위에 아직 남은 카드가 없습니다. 필터를 바꾸거나 초기화해 보세요.</p>
                ) : (
                  visibleQuestions.map((question, index) => {
                    const isActive = index === activeIndex;

                    return (
                      <button
                        key={question.questionId}
                        className={`toc-item ${isActive ? "active" : ""}`}
                        style={{ animationDelay: `${index * 28}ms` }}
                        type="button"
                        onClick={() => handleTocSelect(index)}
                      >
                        <span className="toc-index">{index + 1}</span>
                        <strong>{question.part}</strong>
                        <p>{shorten(getQuestionLabel(question))}</p>
                      </button>
                    );
                  })
                )}
              </div>
            )}
          </>
        )}
      </section>

      {currentQuestion ? (
        <div className={`deck-frame deck-frame--${direction}`} key={currentQuestion.questionId}>
          <QuestionCard
            index={activeIndex}
            meta={`${currentQuestion.unitId} / ${currentQuestion.part} / ${currentQuestion.type}`}
            prompts={currentQuestion.prompts}
          >
            <div className="stack">
              <p className="muted">먼저 답을 떠올리고, 힌트와 정답은 필요할 때만 펼쳐 보세요.</p>

              <div className="study-action-row">
                <button className="secondary" type="button" onClick={() => setShowHint((current) => !current)}>
                  {showHint ? "힌트 닫기" : "힌트 보기"}
                </button>
                <button className="secondary" type="button" onClick={() => setRevealAnswer((current) => !current)}>
                  {revealAnswer ? "정답 숨기기" : "정답 보기"}
                </button>
              </div>

              {showHint ? (
                <div className="hint-box stack">
                  <strong>힌트</strong>
                  <div className="hint-list">
                    <div>
                      <span className="muted">키워드</span>
                      <p>{currentQuestion.keywords.length ? currentQuestion.keywords.join(" / ") : "등록된 키워드 없음"}</p>
                    </div>
                    <div>
                      <span className="muted">연관 표현</span>
                      <p>{currentQuestion.aliases.length ? currentQuestion.aliases.join(" / ") : "등록된 대체 표현 없음"}</p>
                    </div>
                  </div>
                </div>
              ) : null}

              {revealAnswer ? (
                <div className="study-answer stack">
                  <strong>정답</strong>
                  <p>{currentQuestion.answers.join(" / ")}</p>
                </div>
              ) : null}

              <div className="study-action-row">
                <button type="button" onClick={() => handleRemembered(currentQuestion.questionId, true)}>
                  외웠어요
                </button>
                <button
                  className="secondary"
                  type="button"
                  onClick={() => handleRemembered(currentQuestion.questionId, false)}
                >
                  다시 볼래요
                </button>
                <button
                  className="secondary"
                  disabled={activeIndex === 0}
                  type="button"
                  onClick={() => goToIndex(activeIndex - 1, "backward")}
                >
                  이전 카드
                </button>
                <button
                  className="secondary"
                  disabled={activeIndex >= visibleCount - 1}
                  type="button"
                  onClick={() => goToIndex(activeIndex + 1, "forward")}
                >
                  다음 카드
                </button>
              </div>
            </div>
          </QuestionCard>
        </div>
      ) : (
        <section className="panel stack">
          <h2>학습을 시작할 카드가 아직 없습니다.</h2>
          <p className="muted">단원과 파트를 먼저 고르거나, 다른 범위로 바꿔서 다시 시도해 보세요.</p>
          <div className="actions">
            <button type="button" onClick={resetSession}>
              선택 초기화
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
