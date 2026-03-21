import { BackLink } from "@/components/BackLink";
import { ExamSetupForm } from "@/components/ExamSetupForm";
import { getUnits } from "@/lib/api";

export default async function ExamPage() {
  const units = await getUnits();

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">시험 모드</div>
          <h1>범위를 고른 뒤 시험을 만들고, 한 번에 제출해서 결과를 확인합니다.</h1>
          <p className="muted">자동으로 생성하지 않고, 지금부터 풀 시험을 직접 선택해서 시작합니다.</p>
          <div className="actions">
            <BackLink fallbackHref="/" />
          </div>
        </section>

        <section className="grid columns-2">
          <ExamSetupForm units={units} />
          <section className="panel stack">
            <h2>출제 대상 단원</h2>
            {units.map((unit) => (
              <div key={unit.unitId}>
                <strong>{unit.unitId}</strong>
                <p className="muted">
                  파트 {unit.parts.join(", ")} / {unit.questionCount}문제
                </p>
              </div>
            ))}
          </section>
        </section>
      </div>
    </main>
  );
}
