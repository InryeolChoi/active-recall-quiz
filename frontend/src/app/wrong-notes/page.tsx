import Link from "next/link";

import { BackLink } from "@/components/BackLink";
import { WrongNotesClient } from "@/components/WrongNotesClient";

export default function WrongNotesPage() {
  return (
    <main>
      <div className="page">
        <section className="hero stack">
          <div className="badge">오답노트</div>
          <h1>틀린 문제를 모아두고 다시 반복해서 확인합니다.</h1>
          <div className="actions">
            <BackLink fallbackHref="/" />
            <Link className="button secondary" href="/exam">
              새 시험 만들기
            </Link>
          </div>
        </section>
        <WrongNotesClient />
      </div>
    </main>
  );
}
