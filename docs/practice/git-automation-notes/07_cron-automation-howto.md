# 07. 커밋 로그 백업을 위한 크론(Cron) 자동화 설정 가이드

📁 위치: /practice/git-automation-notes/07_cron-automation-howto.md  
📅 정리일: 2025-08-01

---

## 🎯 목적

> 손으로 매번 git log 추출할 필요 없이,  
> 하루에 한 번 자동으로 로컬 저장소의 커밋 메시지를 추출해 `.md`로 저장하는 스케줄을 **cron**으로 등록합니다.  
> 즉, **로그 백업 자동화 시스템**을 구축하는 것이 목표입니다.

---

## 🧩 전체 흐름

```
crontab 등록
    ↓
매일 정해진 시각에 shell script(.sh) 실행
    ↓
git log → Markdown 형식으로 정리
    ↓
docs/changelog/내에 백업 파일 생성 or 덮어쓰기
```

---

## 🛠 사용 스크립트

```
scripts/extract_langchain_commits.sh
```

### 예시 코드:

```
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

output_path="docs/changelog/langchain-commit-message-from-git.md"

{
  echo "# 🧾 커밋 메시지 백업 (자동)"
  echo ""
  git log --pretty=format:"- %ad → %s" --date=format:"%Y-%m-%d %H:%M"
} > "$output_path"
```

📎 로그가 일정한 시간에 Markdown 문서로 자동 생성되며 덮어써집니다.

---

## 🧭 크론 등록 절차

### 1. 크론 편집기 열기

```
crontab -e
```

### 2. 아래 한 줄 추가

```
0 23 * * * /Users/jay/Projects/20250727-langchain-note/scripts/extract_langchain_commits.sh
```

🎯 위 설정은 → **매일 밤 11시에 실행**

---

## 📌 크론 시간 형식 정리

```
분(0~59)  시(0~23)  일(1~31)  월(1~12)  요일(0~6, 0=일)
```

### 예시:

| 크론 표현      | 의미             |
|----------------|------------------|
| `0 11 * * *`   | 매일 오전 11시 실행 |
| `30 18 * * 5`  | 매주 금요일 오후 6시 30분 실행 |

---

## 💡 PATH 설정 이유

크론 환경에서는 `git` 같은 명령어가 기본 경로에 안 잡혀 있을 수 있음 → 오류 방지 필요

```
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
```

💡 꼭 `.sh` 파일 맨 위에 넣어주세요.

---

## 🧪 실행 테스트 Tip

1. 시간을 현재 +2~3분으로 임시 설정
```
56 22 * * * /.../extract_langchain_commits.sh
```

2. 몇 분 뒤 파일이 생성되는지 확인
```
cat docs/changelog/langchain-commit-message-from-git.md
```

---

## 🔄 자동화된 로그 파일

```
docs/changelog/langchain-commit-message-from-git.md
```

✅ 자동으로 매일 덮어쓰이며 최신 git log 메시지를 보관  

❗ **`.gitignore`에 꼭 추가**해두면 깃에 포함되지 않음

---

## ✅ .gitignore 설정 예시

```
# 자동 커밋 로그 파일 (cron에서 생성)

docs/changelog/langchain-commit-message-from-git.md
```

---

## 🛑 문제가 발생했을 때

| 문제 | 원인 / 확인 |
|------|-------------|
| 로그 파일이 안 생김 | 크론이 실행 안 됨 → `crontab -l` 확인, 경로 문제 |
| git 명령어 못 찾음 | `$PATH` 문제 → `export PATH` 적용 필요 |
| 파일이 이상한 데 생김 | 상대경로 문제 → `.sh` 내부에서 `cd $(dirname $0)` 등 사용 고려 |

---

## 🔗 관련 문서

- [01_git-auto-commit-overview.md](./01_git-auto-commit-overview.md)
- [05_gitignore-log-structure.md](./05_gitignore-log-structure.md)

<br>

✅ 다음 문서 →  
📄 [08_path-debug-case-study.md](./08_path-debug-case-study.md): scripts/scripts? 왜 생겼나 경로 이슈 추적기록
