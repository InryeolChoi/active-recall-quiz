"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { GradingResult } from "@/lib/types";
import { appendWrongNotesFromResult } from "@/lib/wrong-note-storage";

type Props = {
  result: GradingResult;
};

export function WrongNoteActions({ result }: Props) {
  const [savedCount, setSavedCount] = useState<number | null>(null);

  useEffect(() => {
    const appendedCount = appendWrongNotesFromResult(result);
    setSavedCount(appendedCount);
  }, [result]);

  if (savedCount === null) {
    return null;
  }

  return (
    <div className="panel stack">
      <h2>오답노트</h2>
      <p className="muted">
        {savedCount > 0
          ? `이번 시험에서 틀린 문제 ${savedCount}개를 오답노트에 저장했습니다.`
          : "이번 시험은 전부 맞아서 새로 저장된 오답이 없습니다."}
      </p>
      <div className="actions">
        <Link className="button secondary" href="/wrong-notes">
          오답노트 보기
        </Link>
      </div>
    </div>
  );
}
