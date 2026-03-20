"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { WrongNoteEntry } from "@/lib/types";
import { readWrongNotes, writeWrongNotes } from "@/lib/wrong-note-storage";

export function WrongNotesClient() {
  const [entries, setEntries] = useState<WrongNoteEntry[]>([]);

  useEffect(() => {
    setEntries(readWrongNotes());
  }, []);

  function clearNotes() {
    writeWrongNotes([]);
    setEntries([]);
  }

  return (
    <section className="panel stack">
      <div className="actions">
        <div className="badge">저장된 오답 {entries.length}</div>
        <button className="secondary" onClick={clearNotes} type="button">
          오답노트 비우기
        </button>
      </div>

      {entries.length === 0 ? (
        <div className="stack">
          <p className="muted">아직 저장된 오답이 없습니다.</p>
          <Link className="button secondary" href="/exam">
            시험 만들러 가기
          </Link>
        </div>
      ) : (
        entries.map((entry) => (
          <article key={entry.id} className="question-card stack">
            <strong>{entry.questionId}</strong>
            <p className="muted">저장 시각 {entry.savedAt}</p>
            <p>{entry.feedback}</p>
            <p className="muted">내 답안: {entry.userAnswer || "(미입력)"}</p>
            <p className="muted">정답: {entry.expectedAnswers.join(" / ")}</p>
            {entry.missingKeywords.length > 0 ? (
              <p className="muted">누락 키워드: {entry.missingKeywords.join(", ")}</p>
            ) : null}
            <div className="actions">
              <Link className="button secondary" href={`/exam/${entry.examId}`}>
                원래 시험 다시 보기
              </Link>
            </div>
          </article>
        ))
      )}
    </section>
  );
}
