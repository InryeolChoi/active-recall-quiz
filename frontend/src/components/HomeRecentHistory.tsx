"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import type { WrongNoteEntry } from "@/lib/types";
import { readWrongNotes } from "@/lib/wrong-note-storage";

function formatSavedAt(savedAt: string) {
  const date = new Date(savedAt);
  if (Number.isNaN(date.getTime())) {
    return savedAt;
  }

  return new Intl.DateTimeFormat("ko-KR", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  }).format(date);
}

export function HomeRecentHistory() {
  const [entries, setEntries] = useState<WrongNoteEntry[]>([]);

  useEffect(() => {
    setEntries(readWrongNotes());
  }, []);

  const recentEntries = useMemo(() => entries.slice(0, 4), [entries]);

  return (
    <section className="panel stack">
      <div className="home-section-head">
        <div className="stack">
          <h2>최근 학습 기록</h2>
          <p className="muted">최근 틀렸던 문제와 다시 볼 포인트를 중심으로 바로 이어서 복습할 수 있어요.</p>
        </div>
        <Link className="button secondary" href="/wrong-notes">
          오답노트 열기
        </Link>
      </div>

      {recentEntries.length === 0 ? (
        <div className="recent-history-empty stack">
          <strong>아직 쌓인 기록이 없습니다.</strong>
          <p className="muted">시험을 풀거나 오답노트를 저장하면 최근 학습 기록이 이곳에 정리됩니다.</p>
          <div className="actions">
            <Link className="button" href="/exam">
              시험 만들어보기
            </Link>
            <Link className="button secondary" href="/study">
              바로 학습하기
            </Link>
          </div>
        </div>
      ) : (
        <div className="recent-history-grid">
          {recentEntries.map((entry) => (
            <article key={entry.id} className="recent-history-card stack">
              <div className="recent-history-meta">
                <strong>{entry.questionId}</strong>
                <span className="muted">{formatSavedAt(entry.savedAt)}</span>
              </div>
              <p>{entry.feedback}</p>
              <p className="muted">내 답안: {entry.userAnswer || "(미입력)"}</p>
              {entry.missingKeywords.length > 0 ? (
                <p className="muted">다시 볼 키워드: {entry.missingKeywords.join(", ")}</p>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
