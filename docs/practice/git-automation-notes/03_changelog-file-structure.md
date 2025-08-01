# 03. 커밋 기록용 md 파일 구조 — 공식 changelog, commit-log, raw-log

📁 위치: /practice/git-automation-notes/03_changelog-file-structure.md  
📅 정리일: 2025-08-01

## 📋 목적

프로젝트 내에서 커밋 메시지와 변경 이력을  
**어떤 .md 파일에, 어떤 기준/형식으로 남겨야 할지** 구분하고,  
운영용 changelog와 실습/백업용 로그의 역할을 명확히 정리합니다.

## 🗂 주요 changelog/md 파일별 역할 비교

| 파일명                                | 주요 쓰임                                             |
|---------------------------------------|-------------------------------------------------------|
| `commit-log.md`                       | 사람이 정리하는 공식/수동 changelog.                    |
| `official.md`                         | milestone(릴리즈/기능단위) 중심 changelog, 공개용.     |
| `py-gen-langchain-commit-log.md`      | 커밋 생성기 CLI가 자동 생성·append하는 raw 메시지 백업. |
| `rebase-track.md`                     | 실수·복구·rebase 등 트러블슈팅 이력용.                 |

## 📑 파일별 용도 상세

### 1. `commit-log.md`

- **핵심:**  
  매일/수시 커밋 메시지 중 사람/관리자가  
  “공식적으로 남겨야 할” 기록만 manual하게 요약/관리

- **권장 포맷:**  
  ```plaintext
  ## 2025-08-01

  - feat[#14.1]: (...중략...)
  - fix[#13.8]: ...
  ```

### 2. `official.md`

- **역할:**  
  milestone(기능 도약·릴리즈·대규모 변화) 단위 요약 changelog  
  공식 릴리즈 로그로 바로 활용 가능

- **예시:**  
  ```plaintext
  ## #14 커밋 자동화 시스템 도입 (2025-08-01)

  - gen_langchain_commit.py CLI 도구 개발
  - 로그 파일 py-gen...md 분리, .gitignore 정책 도입
  ...
  ```

### 3. `py-gen-langchain-commit-log.md`

- **자동화 역할:**  
  `gen_langchain_commit.py`에서 커밋 메시지 입력 시  
  **자동으로 append되는 실제 커밋 메시지 raw 백업**

- **포맷 예시:**  
  ```plaintext
  feat[#14.1]: 자동 커밋 메시지 생성 시스템 도입 및 문서 정리

  - CLI 기반 커밋 생성기 작성
  - 문서 및 구조 정비
  ```

### 4. `rebase-track.md`

- **활용:**  
  히스토리 복구, rebase/merge/충돌, 실수/복구 작업 등  
  일회성이나 수술형 이벤트 이력 별도 관리

## 💡 파일-기능 연결 다이어그램

```plaintext
자동 커밋 메시지 생성기(py) 
   └→ py-gen-langchain-commit-log.md (raw 로그 자동!)
      └→ commit-log.md (관리자 manual 요약)
         └→ official.md (릴리즈 milestone 공식 changelog)
복구/트러블슈팅 situ. 
   └→ rebase-track.md
```

## 🧑💻 실전 관리 체크리스트

- **raw-log는 자동 append, 실명 추적 포함 → .gitignore 미적용 원칙 (백업기능 우선)**
- **commit-log는 milestone 공식 changelog 작성 시 참고**
- **rebase-track.md는 일반 changelog에서 분리, 실수/복구 과정만 기록**

## 🔗 연관 문서

- [01_git-auto-commit-overview.md](./01_git-auto-commit-overview.md)
- [09_commit-log-append-format.md](./09_commit-log-append-format.md)

✅ 다음 →  
📄 [04_commit-numbering-strategy.md](./04_commit-numbering-strategy.md) 커밋 프리픽스/버전 넘버링 전략 정리