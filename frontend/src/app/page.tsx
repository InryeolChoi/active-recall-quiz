import Link from "next/link";

import { getQuestions, getUnits } from "@/lib/api";

export default async function HomePage() {
  const [units, questions] = await Promise.all([getUnits(), getQuestions()]);

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">Markdown 기반 정처기 실기 학습 앱</div>
          <h1>정리한 노트를 그대로 문제 은행으로 바꿔서 외우는 흐름을 만들어요.</h1>
          <p className="muted">
            현재는 느슨한 md 파서, 시험 생성 API, 서술형 채점 흐름까지 연결된 초기 버전입니다.
          </p>
          <div className="actions">
            <Link className="button" href="/study">
              학습 모드 보기
            </Link>
            <Link className="button secondary" href="/exam">
              시험 생성하기
            </Link>
            <Link className="button secondary" href="/wrong-notes">
              오답노트 보기
            </Link>
          </div>
        </section>

        <section className="grid columns-2">
          <div className="panel stack">
            <h2>단원 현황</h2>
            {units.map((unit) => (
              <div key={unit.unitId}>
                <strong>{unit.unitId}</strong>
                <p className="muted">
                  파트 {unit.parts.join(", ")} / 문제 수 {unit.questionCount}
                </p>
              </div>
            ))}
          </div>

          <div className="panel stack">
            <h2>현재 파싱된 문제</h2>
            <p className="muted">총 {questions.length}문제가 로드되었습니다.</p>
            {questions.slice(0, 3).map((question) => (
              <div key={question.questionId}>
                <strong>{question.questionId}</strong>
                <p className="muted">{question.prompts[0]}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
