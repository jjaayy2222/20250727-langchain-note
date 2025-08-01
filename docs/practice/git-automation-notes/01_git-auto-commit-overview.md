# 01. Git 커밋 메시지 자동화 시스템 개요

📅 기록일: 2025-08-01  
📁 위치: /practice/git-automation-notes/

---

## 🧭 목적

> Git 커밋 메시지를 매번 수동으로 입력하는 불편함과 커밋 구조의 비일관성을 줄이고,  
> **반복 가능한 구조화된 커밋 메시지 시스템 + 자동 기록 백업 구조**를 구축한다.

---

## 🛠 시스템 구성 요약

| 구성 요소 | 설명 |
|-----------|------|
| `gen_langchain_commit.py` | Python 기반 CLI 커밋 메시지 생성기 |
| `commit-message-raw-log.md` | CLI 로 입력한 커밋 메시지를 자동 append |
| `gen_langchain_commits.md` | 기능 설명 및 사용법 가이드 문서 |
| `extract_langchain_commits.sh` | 기존 Git 로그를 Markdown 파일로 추출하는 스크립트 |
| `crontab` | 커밋 메시지 자동 백업을 위한 실행 스케줄러 (cron) 등록 |
| `.gitignore` | 캐시, 자동 생성 로그 등 Git 추적 대상 제외 설정 |

---

## 🧩 전체 흐름

```plaintext
사용자 입력
    ↓
gen_langchain_commit.py 실행
    ↓
입력: 타입 / prefix / 제목 / 본문
    ↓
git add . && git commit -m "{정형화된 메시지}"
    ↓
commit-message-raw-log.md 에 자동 저장
```

---

## 🧱 구축하면서 사용한 주요 기술 요소

- Python CLI 인터페이스 (print + input + prefix 캐싱)
- `git status`, `git log`, `git add`, `git reset` 활용
- `Path(__file__).resolve().parent` 기반 경로 정리
- soft reset을 활용한 커밋 undo & 재작성
- Markdown 기반 changelog 3단 구분 (`commit-log.md`, `official.md`, `raw-log.md`)
- `.gitignore` 전략적 구성

---

## 💬 실사용 예시

```
$ ./gen_langchain_commit.py
→ 타입 선택: 1(feat)
→ prefix: 14.1
→ 제목: 자동 커밋 메시지 생성 시스템 도입
→ 본문: 커밋 생성기 + 문서 + .gitignore 정비
→ git commit + 로그 파일에 자동 기록
```

자동 생성 로그 예시 (`docs/changelog/py-gen-langchain-commit-log.md`):

```
feat[#14.1]: 자동 커밋 메시지 생성 시스템 도입 및 문서 정리

- CLI 기반 커밋 생성기 작성
- 문서 및 구조 정비
- 자동 로그 및 캐시 파일 정리
```

---

## 🔗 연관된 문서

- [02_commit-msg-cli-usage.md](./02_commit-msg-cli-usage.md)
- [03_changelog-file-structure.md](./03_changelog-file-structure.md)
- [07_cron-automation-howto.md](./07_cron-automation-howto.md)

---

✅ 다음 문서:  
📄 [02_commit-msg-cli-usage.md → CLI 사용법 정리](./02_commit-msg-cli-usage.md)
