# 02. Git 커밋 메시지 자동 생성기 — CLI 사용법

📁 위치: /practice/git-automation-notes/02_commit-msg-cli-usage.md  
📅 정리일: 2025-08-01

---

## 🎯 이 문서는 무엇인가요?

본 문서는 `scripts/gen_langchain_commit.py` 를 사용하여  
**커밋 메시지를 일관되고 구조적으로 생성하고 커밋하는 전체 흐름**을 정리합니다.  
사용자와 터미널 사이에서 어떤 입력이 오고 가는지, 어떤 규칙이 있는지를 예시 중심으로 소개합니다.

---

## 🧩 전체 사용 흐름

```
사용자 입력
    ↓
gen_langchain_commit.py 실행
    ↓
입력: 타입 / prefix / 제목 / 본문
    ↓
git add . && git commit -m "{정형화된 메시지}"
    ↓
py-gen-langchain-commit-log.md 에 자동 저장
```

---

## 🛠 실행 방법

터미널에서 아래와 같이 실행합니다:

```
python scripts/gen_langchain_commit.py
# 또는
./scripts/gen_langchain_commit.py
# 실행 권한 부여가 안 되어 있다면:
chmod +x scripts/gen_langchain_commit.py
```

---

## 💬 입력 단계 설명

| 입력 항목 | 설명 |
|-----------|------|
| 타입 선택 | `feat`, `fix`, `docs`, `chore`, `refactor`, `build` 중 하나를 번호로 선택 |
| prefix 입력 | `#14.1`처럼 커밋 버전 넘버링: Enter 시 최근 prefix를 기준으로 자동 제안 |
| 제목 입력 | 한 줄 제목 입력 — 커밋 핵심 요약 |
| 본문 입력 | 여러 줄 입력 가능 (줄마다 Enter, 마지막에 “빈 줄” 입력 시 종료됨) |
| 커밋 전 확인 | 최종 메시지를 출력하여 커밋 여부를 묻는 확인 단계 |
| 커밋 수행 | `git add .` → `git commit` → 로그 파일에 append 처리까지 자동 |

---

## 🧪 예시 세션

```plaintext
📝 변경된 파일:
  · README.md
  · gen_langchain_commit.py
----------------------------------------

커밋 타입:
1) feat  2) fix  3) docs  4) chore  5) refactor  6) build  
번호 선택 (Enter=1): 1

prefix[#번호] (Enter=14.1): 
커밋 제목 (Enter=커밋 생성기 기능 완성): 커밋 생성기 기능 완성

커밋 본문 (여러 줄, 빈 줄로 종료):
- 커밋 타입/번호/제목 자동 입력 지원
- git status 기반 변경 파일 안내 출력
- 자동 prefix 증가 및 캐싱 적용

🧾 최종 메시지:
========================================
feat[#14.1]: 커밋 생성기 기능 완성

- 커밋 타입/번호/제목 자동 입력 지원
- git status 기반 변경 파일 안내 출력
- 자동 prefix 증가 및 캐싱 적용
========================================

🚀 이 메시지로 커밋하시겠습니까? (y/n): y
✅ 커밋 완료!
```

---

## 🗃 자동 저장 로그 위치

```
📁 docs/changelog/py-gen-langchain-commit-log.md
```

💡 모든 커밋 메시지는 이 파일에 **형식 유지된 상태로 append** 됩니다.  
버전별 커밋 메시지를 추적하는 백업 겸 changelog raw 자료로 활용됩니다.

---

## 🔐 캐시 파일 생성 위치

```
📁 scripts/gen_langchain_commit_cache.json
```

- 최근 사용한 커밋 타입, prefix, 제목을 기억합니다.
- 다음 실행 시 자동으로 기본값으로 당겨옵니다.
- 이 파일은 .gitignore에 등록하여 Git에 포함시키지 않습니다.

---

## 🧼 에러/실수 방지 팁

| 문제 상황 | 대응 방법 |
|------------|------------|
| 커밋 메시지를 수정하고 싶을 때 | 커밋 직후 `git reset --soft HEAD~1` 후 재실행 |
| 커밋 메시지 중복 작성 방지 | prefix 숫자 증가 여부 직접 체크 or 자동 제안 사용 |
| 파일 경로 이상하게 생성됨 | Path 모듈 사용하여 절대경로 기반으로 코드 수정 ✔ |

---

## 🔗 관련 문서

- [01_git-auto-commit-overview.md](./01_git-auto-commit-overview.md) — 전체 시스템 개요
- [04_commit-numbering-strategy.md](./04_commit-numbering-strategy.md) — 프리픽스 관리 기준
- [09_commit-log-append-format.md](./09_commit-log-append-format.md) — 자동 로그 포맷 예시

---

✅ 다음 문서 →  
📄 [03_changelog-file-structure.md](./03_changelog-file-structure.md): commit-log.md / official.md / raw-log.md 구조 비교
