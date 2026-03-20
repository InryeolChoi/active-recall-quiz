"use client";

import { useMemo, useState, useTransition } from "react";
import { useRouter } from "next/navigation";

import { createExam } from "@/lib/api";
import { UnitSummary } from "@/lib/types";

type Props = {
  units: UnitSummary[];
};

export function ExamSetupForm({ units }: Props) {
  const router = useRouter();
  const [selectedUnitId, setSelectedUnitId] = useState(units[0]?.unitId ?? "");
  const [selectedPart, setSelectedPart] = useState("");
  const [questionCount, setQuestionCount] = useState(5);
  const [shuffle, setShuffle] = useState(false);
  const [mode, setMode] = useState<"study" | "exam">("exam");
  const [error, setError] = useState("");
  const [isPending, startTransition] = useTransition();

  const selectedUnit = useMemo(
    () => units.find((unit) => unit.unitId === selectedUnitId),
    [selectedUnitId, units]
  );

  async function handleCreateExam() {
    setError("");
    startTransition(async () => {
      try {
        const exam = await createExam({
          unitIds: selectedUnitId ? [selectedUnitId] : [],
          parts: selectedPart ? [selectedPart] : [],
          questionCount,
          mode,
          shuffle
        });
        router.push(`/exam/${exam.examId}`);
      } catch (createError) {
        setError(createError instanceof Error ? createError.message : "시험 생성에 실패했습니다.");
      }
    });
  }

  return (
    <section className="panel stack">
      <h2>시험 만들기</h2>
      <label className="stack">
        <span>단원</span>
        <select value={selectedUnitId} onChange={(event) => setSelectedUnitId(event.target.value)}>
          {units.map((unit) => (
            <option key={unit.unitId} value={unit.unitId}>
              {unit.unitId} ({unit.questionCount}문제)
            </option>
          ))}
        </select>
      </label>

      <label className="stack">
        <span>파트</span>
        <select value={selectedPart} onChange={(event) => setSelectedPart(event.target.value)}>
          <option value="">전체</option>
          {selectedUnit?.parts.map((part) => (
            <option key={part} value={part}>
              {part}
            </option>
          ))}
        </select>
      </label>

      <label className="stack">
        <span>문제 수</span>
        <input
          min={1}
          max={selectedUnit?.questionCount ?? 100}
          type="number"
          value={questionCount}
          onChange={(event) => setQuestionCount(Number(event.target.value))}
        />
      </label>

      <label className="stack">
        <span>시험 모드</span>
        <select value={mode} onChange={(event) => setMode(event.target.value as "study" | "exam")}>
          <option value="exam">실전 모드</option>
          <option value="study">복습 모드</option>
        </select>
      </label>

      <label className="checkbox-row">
        <input
          checked={shuffle}
          type="checkbox"
          onChange={(event) => setShuffle(event.target.checked)}
        />
        <span>문제 순서를 섞어서 출제하기</span>
      </label>

      <p className="muted">
        선택한 범위에서 최대 {selectedUnit?.questionCount ?? 0}문제까지 불러옵니다.
      </p>
      {error ? <p className="error-text">{error}</p> : null}
      <button onClick={handleCreateExam} disabled={isPending || units.length === 0}>
        {isPending ? "시험 만드는 중..." : "시험 시작하기"}
      </button>
    </section>
  );
}
