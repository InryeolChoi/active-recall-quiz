import Link from "next/link";

import { ExamClient } from "@/app/exam/[examId]/ExamClient";
import { getExam } from "@/lib/api";

type Props = {
  params: Promise<{ examId: string }>;
};

export default async function ExamDetailPage({ params }: Props) {
  const { examId } = await params;
  const exam = await getExam(examId);

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">실전 연습</div>
          <h1>{exam.questionCount}문제를 서술형으로 풀어보세요.</h1>
          <p className="muted">
            생성 시각 {exam.createdAt} / 범위 {exam.unitIds.join(", ") || "전체"}
            {exam.parts.length > 0 ? ` / ${exam.parts.join(", ")}` : ""}
          </p>
          <div className="actions">
            <Link className="button secondary" href="/exam">
              시험 설정으로 돌아가기
            </Link>
          </div>
        </section>
        <ExamClient exam={exam} />
      </div>
    </main>
  );
}
