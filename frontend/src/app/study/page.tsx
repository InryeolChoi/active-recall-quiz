import { QuestionCard } from "@/components/QuestionCard";
import { getQuestions } from "@/lib/api";

export default async function StudyPage() {
  const questions = await getQuestions();

  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">학습 모드</div>
          <h1>문제를 보고 먼저 떠올린 뒤, 바로 정답을 확인합니다.</h1>
          <p className="muted">초기 버전이라 정답을 함께 보여주고, 이후에는 가림/오답노트 기능을 추가하면 됩니다.</p>
        </section>

        <section className="grid">
          {questions.map((question, index) => (
            <QuestionCard
              key={question.questionId}
              index={index}
              prompts={question.prompts}
              meta={`${question.unitId} / ${question.part} / ${question.type}`}
            >
              <div className="panel">
                <strong>정답</strong>
                <p>{question.answers.join(" / ")}</p>
              </div>
            </QuestionCard>
          ))}
        </section>
      </div>
    </main>
  );
}
