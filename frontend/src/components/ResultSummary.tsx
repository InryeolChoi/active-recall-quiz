import { GradingResult } from "@/lib/types";
import { WrongNoteActions } from "@/components/WrongNoteActions";
import Link from "next/link";

type Props = {
  result: GradingResult;
};

export function ResultSummary({ result }: Props) {
  const correctCount = result.results.filter((item) => item.isCorrect).length;
  const wrongCount = result.results.length - correctCount;

  return (
    <section className="panel stack">
      <div className="actions">
        <div className="badge">
          총점 {result.score} / {result.total}
        </div>
        <div className="badge secondary-badge">정답 {correctCount}</div>
        <div className="badge secondary-badge">오답 {wrongCount}</div>
      </div>
      <div className="actions">
        <Link className="button" href={`/exam/${result.examId}`}>
          같은 시험 다시 보기
        </Link>
        <Link className="button secondary" href="/wrong-notes">
          오답노트 보기
        </Link>
        <Link className="button secondary" href="/exam">
          새 시험 만들기
        </Link>
      </div>
      <WrongNoteActions result={result} />
      {result.results.map((item) => (
        <article key={item.questionId} className="question-card stack">
          <strong>{item.questionId}</strong>
          <p>{item.feedback}</p>
          <p className="muted">내 답안: {item.userAnswer || "(미입력)"}</p>
          <p className="muted">모범 답안: {item.expectedAnswers.join(" / ")}</p>
          {item.missingKeywords.length > 0 ? (
            <p className="muted">누락 키워드: {item.missingKeywords.join(", ")}</p>
          ) : null}
        </article>
      ))}
    </section>
  );
}
