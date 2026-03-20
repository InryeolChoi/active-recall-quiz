import Link from "next/link";

import { ResultSummary } from "@/components/ResultSummary";
import { getExamResult } from "@/lib/api";

type Props = {
  params: Promise<{ examId: string }>;
};

export default async function ResultPage({ params }: Props) {
  const { examId } = await params;
  const result = await getExamResult(examId);

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">채점 결과</div>
          <h1>맞은 부분과 빠진 키워드를 한눈에 봅니다.</h1>
          <div className="actions">
            <Link className="button secondary" href="/exam">
              다른 시험 만들기
            </Link>
          </div>
        </section>
        <ResultSummary result={result} />
      </div>
    </main>
  );
}
