## 👥 Agent Rules

- 각 쓰레드는 하나의 브랜치를 담당한다
- 각 쓰레드는 고유한 git user.name을 사용한다
- 역할을 벗어난 작업은 수행하지 않는다

---

## 📬 PR Rules

- 모든 결과는 PR 형태로 제출한다
- PR 템플릿을 반드시 사용한다
- PR 본문에 반드시 포함:
  Closes #이슈번호

---

## 🏷 Labels

- theory / frontend / backend

---

## 📦 Repository Scope

- 이 저장소는 학습 노트 자체를 원본으로 보관하지 않는다.
- 학습 노트의 원본은 `active-recall-notes` 저장소에 있다.
- 이 저장소는 CI/CD로 동기화된 데이터를 받아 SQLite에 저장하고, 시험/학습 경험을 제공한다.
- `unit_*` 폴더는 더 이상 이 저장소의 기본 작업 단위가 아니다.

---

## 🟢 Workflow (🔥 중요)

1. 작업 시작 전 반드시 Issue 생성
2. Issue 번호 기반 브랜치 생성
   (ex: feature/12-login)
3. 작업 수행
4. PR 생성

---

## 🌿 Branch Rules

- main 직접 수정 금지
- 모든 작업은 feature/* 브랜치에서 진행

브랜치 네이밍 규칙:
- feature/{issue-number}-{name}
- fix/{issue-number}-{name}
- refactor/{issue-number}-{name}

---

## 📁 Directory Ownership (🔥 핵심)

- /backend → backend agent만 수정 가능
- /frontend → frontend agent만 수정 가능
- /shared → PM만 수정 가능

⚠️ 다른 영역 수정 금지
⚠️ `unit_*` 디렉토리 생성/수정 금지

---

## 🧭 Role Boundaries

- PM
  - Issue 생성
  - 작업 분해
  - 우선순위 설정
  - 다른 agent에게 작업 할당
- backend
  - 데이터 동기화 파이프라인
  - SQLite 저장 구조
  - API 및 서버 로직
- frontend
  - 사용자 화면
  - API 연동
  - 학습/시험/결과 UI

---

## ✅ Change Policy

- 이 저장소에서 문서나 설정을 바꿀 때는 현재 아키텍처와 충돌하지 않는지 먼저 확인한다.
- 새 이론/노트 콘텐츠는 이 저장소가 아니라 `active-recall-notes` 쪽에서 관리한다.
- 기존 `unit_*` 관련 언급은 레거시로만 취급하며, 신규 작업 기준으로 사용하지 않는다.
