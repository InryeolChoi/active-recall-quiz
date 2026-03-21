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

---

## 📁 Special Rule: unit_* (정처기 이론 폴더)

unit_* 디렉토리는 공유 문서 영역이다.

### 역할
- Author: 이론 작성 및 구조 설계
- Fix agent: 오타 및 개념 오류 수정
- Reviewer: 내용 검증 및 승인

### 수정 규칙
- 기존 내용을 전체 삭제 금지
- 필요한 부분만 수정 (diff 기반)
- 구조 변경은 Reviewer 승인 필요

### 브랜치 규칙
- feature/unit-* → 신규 이론 작성
- fix/unit-* → 오류 수정
- refactor/unit-* → 구조 개선

### 충돌 방지
- 하나의 unit 파일은 동시에 하나의 agent만 작업
- 작업 시작 시 Issue로 해당 파일을 명시 (lock 역할)

### 리뷰
- 모든 unit_* 변경은 PR 리뷰 필수
- Reviewer 승인 없이 merge 금지

---

## 📝 Author Workflow (Exception)

- Author는 unit_* 초안을 main에 직접 작성할 수 있다
- 단, 반드시 markdown 검사기를 통해 정제해야 한다
- 최종 품질은 fix PR로 관리한다
