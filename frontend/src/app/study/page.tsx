import { BackLink } from "@/components/BackLink";
import { StudyDeck } from "@/components/StudyDeck";
import { getQuestions, getUnits } from "@/lib/api";

export default async function StudyPage() {
  const [units, questions] = await Promise.all([getUnits(), getQuestions()]);

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">학습 모드</div>
          <h1>단원과 파트를 고르고, 카드 한 장씩 넘기며 회상합니다.</h1>
          <p className="muted">
            목차를 보고 범위를 좁힌 뒤, 힌트와 정답을 단계적으로 펼치면서 셀프 체크할 수 있습니다.
          </p>
          <div className="actions">
            <BackLink fallbackHref="/" />
          </div>
        </section>

        <StudyDeck questions={questions} units={units} />
      </div>
    </main>
  );
}
