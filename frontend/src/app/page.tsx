import Link from "next/link";
import { HomeRecentHistory } from "@/components/HomeRecentHistory";

export default async function HomePage() {
  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">Markdown 기반 정처기 실기 학습 앱</div>
          <h1>정리한 노트를 그대로 문제 은행으로 바꿔서 외우는 흐름을 만들어요.</h1>
          <p className="muted">최근 학습 흐름을 이어 보고, 시험과 오답노트까지 한 번에 연결해서 반복 회상을 만들 수 있어요.</p>
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

        <HomeRecentHistory />
      </div>
    </main>
  );
}
