# 08. 경로 꼬임/파일 중복 생성 디버깅 사례 — scripts/scripts 문제 파헤치기

📁 위치: /practice/git-automation-notes/08_path-debug-case-study.md  
📅 정리일: 2025-08-01

---

## 🎯 목적

자동화 시스템 도입 시,
“내가 원하지 않은 경로(scripts/scripts 등)에 파일이 생기는”  
가장 흔하면서 답답한 문제의 원인과 해결 과정을 Jay가 직접 겪은 실전 흐름으로 정리합니다.

---

## 🧩 문제 발생 상황

### 현상

- 커밋 메시지 자동 생성기 CLI를 사용하다 보니…
    - `scripts/scripts/gen_commit_cache.json`
    - `scripts/scripts/generate_commits.md`
    - `scripts/docs/changelog/commit-message-raw-log.md`
      같은 **중복 경로/폴더**에 파일이 쌓임

- 원래 의도:
    - 캐시 파일: `scripts/gen_langchain_commit_cache.json`
    - 문서: `docs/changelog/...`

---

## 🕵️‍♂️ 원인 분석

### 1. 파이썬 상대 경로의 함정

- 코드에서 단순히  
  ```
  LOG_PATH = "docs/changelog/py-gen-langchain-commit-log.md"
  ```
  이렇게 적으면  
  **실행 위치(PWD) 기준**으로 파일이 생성됨

    - 예) `/Users/jay/Projects/.../` 폴더에서
      ```
      python scripts/gen_langchain_commit.py
      ```
      → 정상위치에 생성

    - 예) `scripts/` 폴더 내부에서
      ```
      cd scripts/
      python gen_langchain_commit.py
      ```
      → `scripts/docs/...`/`scripts/scripts/...`에 생성

### 2. 자신의 __file__ 위치와 상관없이 실행 디렉토리 따라가는 상대경로 문제

---

## 🔑 해결 전략

### 1. 경로를 항상 **프로젝트 루트 기준 절대 경로로 지정**

#### 코드 예시

```
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
LOG_PATH = project_root / "docs/changelog/py-gen-langchain-commit-log.md"
CACHE_PATH = project_root / "scripts/gen_langchain_commit_cache.json"
```

- `Path(__file__).resolve().parent.parent`로  
  py 스크립트가 어디서 실행되든, 항상 루트 경로 기준으로 파일 생성

### 2. 잘못 생성된 파일 이동/삭제

- 기존에 이미 잘못 쌓인 중복 파일은 수동으로 정리
    ```
    rm -rf scripts/scripts/
    rm -rf scripts/docs/
    ```

---

## 🧪 실전 디버깅 흐름 예시

```
1. 커밋 생성기 돌릴 때마다 scripts/scripts/~, scripts/docs/~ 파일 생김
2. git status에서 자꾸 중복 새 파일이 올라옴
3. py 파일 내부 경로를 Path 객체로 고정 - 한 번에 문제 해결!
4. 기존 꼬인 파일 정리, add 다시 하고 커밋 → 완전히 안정화 완료
```

---

## 📋 팁: 경로 꼬임 실전 예방 포인트

- 항상 **`Path(__file__)` 기준** + `parent`로 경로 관리
- 상대경로 문자열만 쓰면 실행 폴더 바뀔 때마다 오동작 발생함!
- `Git` 자동화 도구 쓸 때 스크립트 실행 위치를 여러 번 테스트해볼 것
- `.gitignore`에 **수동으로 남은 쓸모없는 캐시,`log`도 꼭 첨가**

---

## 📝 내 경험 

> “경로 한 줄이 잘못되면, 하루 종일 커밋 메시지도, 백업 로그도, 모든 파일이 미로처럼 꼬일 수 있다.  
> 결국 한 번은 왜 저기 생기는지 경로를 직접 들여다봐야 비로소 시작된다.” – Jay 😭

---

## 🔗 관련 문서

- [05_gitignore-log-structure.md](./05_gitignore-log-structure.md)
- [06_git-commit-reset-guide.md](./06_git-commit-reset-guide.md)

<br>

✅ 다음 문서 →  
📄 [09_commit-log-append-format.md](./09_commit-log-append-format.md): 커밋 메시지가 markdown으로 어떻게 기록되는지 포맷/구조 사례
