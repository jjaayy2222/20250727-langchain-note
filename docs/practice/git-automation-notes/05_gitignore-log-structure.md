# 05. 자동 생성 로그 및 캐시 파일 gitignore 설계 전략

📁 위치: /practice/git-automation-notes/05_gitignore-log-structure.md  
📅 정리일: 2025-08-01

---

## 🎯 목적

> 자동 커밋 시스템에서 생성되는 로그, 캐시, 백업 파일 중  
> 어떤 파일을 Git에서 추적하고,  
> 어떤 파일은 `.gitignore` 를 통해 제외해야 할지 확실하게 정리합니다.

---

## 📂 자동 커밋 시스템이 생성하는 파일 구분

| 파일 경로                                             | 생성 주체                     | Git 추적 여부       |
|--------------------------------------------------------|-------------------------------|---------------------|
| `docs/changelog/py-gen-langchain-commit-log.md`        | 커밋 CLI 도구 (자동 append)   | ✅ Git에 포함 (추적)  |
| `scripts/gen_langchain_commit_cache.json`              | 커밋 CLI 도구 (입력 캐싱)     | ❌ Git에 포함 ❌      |
| `docs/changelog/langchain-commit-message-from-git.md`  | bash 추출 스크립트 (sh 파일)  | ❌ Git에 포함 ❌      |

---

## ✅ 어떤 기준으로 .gitignore에 넣을까?

### 🟢 Git으로 추적해야 할 파일

| 포함 이유                          |
|----------------------------------|
| 문서의 일부 (공식 changelog 포함 또는 raw 로그 데이터) |
| 다른 개발자도 함께 보고 관리할 changelog |

→ 예:

```
docs/changelog/py-gen-langchain-commit-log.md
```

> 자동으로 써지더라도, 이는 하나의 **공식 커밋 메시지 이력**이므로 추적 OK

---

### 🔴 Git에서 추적하면 안 되는 파일

| 제외 이유                                           |
|------------------------------------------------------|
| 실행할 때마다 달라지는 캐시/로그 | 개인 설정이므로 협업 시 충돌 위험 |
| 다른 사용자에게 의미 없는 machine-specific 결과물  |

→ 예:

```
scripts/gen_langchain_commit_cache.json
docs/changelog/langchain-commit-message-from-git.md
```

그래서 `.gitignore`에는 다음을 포함해야 합니다:

```
# 자동 생성 캐시 & 로그 (Git 추적 제외 대상)
scripts/gen_langchain_commit_cache.json
docs/changelog/langchain-commit-message-from-git.md
````

---

## 🧠 커밋 실패/혼동을 방지하기 위한 실천 팁

- 자동 도구가 생성하는 모든 파일의 경로와 쓰임을 분명히 하고,
- `.gitignore`에 포함 여부를 기록 문서로 명시해 둘 것
- 커밋 전 `git status`에서 "무의미한 파일이 올라가고 있지는 않은가?" 항상 점검

---

## ✅ 최종 체크리스트

| 파일 위치                                | Git에 포함? | 설명                                            |
|------------------------------------------|-------------|-------------------------------------------------|
| docs/changelog/py-gen-langchain-commit-log.md | ✅          | 자동 로그이지만 changelog로 간주                   |
| scripts/gen_langchain_commit_cache.json       | ❌          | 사용자만 참고하는 캐시 파일                        |
| docs/changelog/langchain-commit-message-from-git.md | ❌    | 매일 새로 백업되는 raw 로그 결과물 (bash 기반 추출) |

---

## 🔗 관련 문서

- [02_commit-msg-cli-usage.md](./02_commit-msg-cli-usage.md)
- [09_commit-log-append-format.md](./09_commit-log-append-format.md)

<br>

✅ 다음 문서 →  
📄 [06_git-commit-reset-guide.md](./06_git-commit-reset-guide.md): 커밋 실수 시 되돌리는 reset 전략 가이드
