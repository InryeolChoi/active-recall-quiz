"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { AnswerInput } from "@/components/AnswerInput";
import { QuestionCard } from "@/components/QuestionCard";
import { submitExam } from "@/lib/api";
import { ExamDetail } from "@/lib/types";

type Props = {
  exam: ExamDetail;
};

export function ExamClient({ exam }: Props) {
  const router = useRouter();
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const answeredCount = exam.questions.filter((question) => (answers[question.questionId] ?? "").trim()).length;
  const unansweredCount = exam.questions.length - answeredCount;

  async function handleSubmit() {
    setError("");
    setIsSubmitting(true);
    try {
      const payload = exam.questions.map((question) => ({
        questionId: question.questionId,
        responseText: answers[question.questionId] ?? ""
      }));
      await submitExam(exam.examId, payload);
      router.push(`/results/${exam.examId}`);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "시험 제출에 실패했습니다.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="stack">
      <section className="panel stack exam-status">
        <div className="actions">
          <div className="badge">
            답안 작성 {answeredCount} / {exam.questions.length}
          </div>
          <div className="badge secondary-badge">미작성 {unansweredCount}</div>
        </div>
        <p className="muted">
          빈칸으로 제출해도 채점은 가능하지만, 실전처럼 끝까지 적어보는 쪽이 더 좋습니다.
        </p>
        {error ? <p className="error-text">{error}</p> : null}
      </section>

      {exam.questions.map((question, index) => (
        <QuestionCard
          key={question.questionId}
          index={index}
          prompts={question.prompts}
          meta={`${question.unitId} / ${question.part} / ${question.type}`}
        >
          <AnswerInput
            value={answers[question.questionId] ?? ""}
            onChange={(nextValue) =>
              setAnswers((current) => ({
                ...current,
                [question.questionId]: nextValue
              }))
            }
          />
        </QuestionCard>
      ))}

      <section className="panel stack submit-panel">
        <h2>제출하기</h2>
        <p className="muted">
          다 적었으면 아래 버튼으로 제출하세요. 채점 결과와 오답노트는 제출 후 바로 이어집니다.
        </p>
        <div className="actions">
          <button onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting ? "채점 중..." : "제출하고 채점 보기"}
          </button>
        </div>
      </section>
    </div>
  );
}
