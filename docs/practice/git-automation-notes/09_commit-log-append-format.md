# 09. 커밋 메시지 자동 기록 포맷 구조 안내

📁 위치: /practice/git-automation-notes/09_commit-log-append-format.md  
📅 정리일: 2025-08-01

---

## 🎯 목적

> 커밋 생성기 CLI 도구를 통해 작성한 커밋 메시지가  
> 어떻게 `.md` 형식으로 자동 기록되는지 구조와 포맷을 설명하고,  
> 수동 작성 changelog와는 어떤 차이가 있는지 이해하기 위한 문서입니다.

---

## 🧩 전체 흐름

```
사용자 커밋 입력
    ↓
gen_langchain_commit.py 실행
    ↓
커밋 메시지 생성 → stdout 출력
    ↓
docs/changelog/py-gen-langchain-commit-log.md           # 자동 append
```

---

## 📄 기록되는 파일

> 📍 docs/changelog/py-gen-langchain-commit-log.md

✅ 이 파일은 커밋 메시지 생성기에서 입력한  
전체 커밋 메시지를 Markdown 포맷 그대로 아래처럼 append합니다:

---

### ✍️ 예시 출력:

```
feat[#14.1]: 자동 커밋 메시지 생성 시스템 도입 및 문서 정리

- CLI 커밋 생성기 작성
- 문서/공식 changelog/로그 백업 구조 정비
````

> 줄 간격이 깨지지 않는 형태로 저장  
> 두 줄을 기준으로: **제목 + 본문**을 구분

---

## 🔧 명확한 구조

| 구성 요소       | 설명                                           |
|----------------|------------------------------------------------|
| 커밋 헤드라인   | `feat[#14.1]: ...` 의 형식 → 타입 + prefix + 제목 |
| 본문            | 리스트형으로 바뀌는 내용을 복수 줄로 작성 가능      |
| 구분 방식       | 제목 ↔ 본문 사이에 빈 줄 1줄 포함 (`\n\n`)          |

---

## 🧪 코드 측 처리 방식

```
message = f"{type}[#{prefix}]: {title}"

if body:
    message += f"\n\n{body}"

# 파일 append 코드 ↓
with open(LOG_PATH, "a") as f:
    f.write(message + "\n")
```

- 로그는 별도 날짜 구분 없이 append되며,
- 필요 시 수동으로 날짜 구분 모듈도 later 확장 가능

---

## 📎 수동 changelog와의 차이점

| 구분                          | 공식 changelog (수작업) | 자동 커밋 메시지 로그 |
|-------------------------------|--------------------------|------------------------|
| 관리 주체                     | 사용자 수동 입력         | 커밋 생성기 자동 처리   |
| 기록 시간 구분                 | 날짜 섹션 등 수동 관리    | chronological append    |
| 릴리즈 요약/기능 정리 정교함 | ✅                      | ❌ 간결 메시지 중심      |
| 정확성 (실제 커밋 그대로)     | 유동적 (요약됨)          | ✅ 항상 full copy       |

---

## 🧠 파일 관리 팁

- 커밋 메시지가 자동 누적되기 때문에 → 📈 분석 or changelog 추출도 가능
- `.gitignore`에 포함하지 않으면 백업 역할로 완벽
- 너무 커지는 경우:
    - 연도별 파일 분리 (`py-gen-2025.md`)
    - 날짜 섹션 자동 추가 기능 도입 (확장 가능)

---

## 🔗 유관 문서

- [03_changelog-file-structure.md](./03_changelog-file-structure.md)
- [05_gitignore-log-structure.md](./05_gitignore-log-structure.md)
- [10_dev-journal-2025-08-01.md](./10_dev-journal-2025-08-01.md)

<br>

✅ 다음 문서 →  
📄 [10_dev-journal-2025-08-01.md](./10_dev-journal-2025-08-01.md): Jay의 커밋 자동화 여정 회고 다이어리
