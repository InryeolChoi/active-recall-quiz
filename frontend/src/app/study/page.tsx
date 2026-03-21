import { BackLink } from "@/components/BackLink";
import { StudyDeck } from "@/components/StudyDeck";
import { getQuestions } from "@/lib/api";

export default async function StudyPage() {
  const questions = await getQuestions();

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">학습 모드</div>
          <h1>문제를 보고 먼저 떠올린 뒤, 바로 정답을 확인합니다.</h1>
          <p className="muted">정답을 가렸다가 펼치고, 외운 문제는 숨기면서 반복 회상할 수 있습니다.</p>
          <div className="actions">
            <BackLink fallbackHref="/" />
          </div>
        </section>

        <StudyDeck questions={questions} />
      </div>
    </main>
  );
}
