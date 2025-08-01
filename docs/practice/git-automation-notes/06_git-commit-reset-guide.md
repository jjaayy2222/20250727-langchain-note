# 06. Git 커밋/리셋 실전 가이드 — 실수, 복구, 재작성까지

📁 위치: /practice/git-automation-notes/06_git-commit-reset-guide.md  
📅 정리일: 2025-08-01

---

## 🚦 목적

자동 커밋/문서화 환경에서도  
**실수로 잘못 커밋했거나, 메시지를 다시 쓰고 싶거나, 중복/누락 상황에 처했을 때**  
가장 안전하게 복구할 수 있는 “실전 Git 명령어”를 치트키처럼 정리합니다.

---

## 🗓️ 가장 흔하게 겪는 시나리오 Best 4

| 상황                               | 추천 reset 전략              |
|-------------------------------------|------------------------------|
| 커밋 메시지 오타, 내용 수정 필요    | `git reset --soft HEAD~1`    |
| git add만 하고 commit 전 수정 필요  | `git restore --staged <file>`|
| 커밋+작업까지 완전 취소            | `git reset --hard HEAD~1`    |
| 커밋 여러개 제거 후 재커밋 필요     | `git reset --soft HEAD~N`    |

---

## 🛠 핵심 명령어 설명

```
git reset --soft HEAD~N
```
- 최근 N개 커밋을 삭제하고, 해당 변경 내용은 모두 스테이징 상태로 남겨둡니다.
- 커밋 메시지·내용만 바꿀 때 가장 안전.

```
git reset --mixed HEAD~N
```
- 커밋도, add도 취소. 변경 파일은 워킹 디렉토리 그대로 유지.
- “다시 새로 git add . 선택”부터 시작하고 싶을 때.

```
git reset --hard HEAD~N
```
- 최근 N개 커밋 전체(작업물 포함) 완전히 삭제.
- 되돌릴 수 없으니, 정말 QR코드 찍은 상태에서만.

```
git restore --staged <file>
```
- 파일을 스테이징 영역에서만 꺼내고, 작업 내역은 그대로 워킹 디렉토리에 남긴다.

---

## 🧪 실전 예시

### 1. 메시지 실수/중복 커밋 두 번 했을 때

```
git log --oneline -n 3
git reset --soft HEAD~2
# 다시 git add . (or 필요한 파일만)
# 커밋 생성기 재실행
```

### 2. git add만 실수로 했다면

```
git restore --staged <file>
# 워킹디렉토리 파일만 남고, 스테이징에서 빠짐
```

---

## 💡 복구 팁/주의사항

- 커밋 내리고 나면, 항상 `git status`로 내 파일에 빠짐없이 올라왔는지 직접 점검!
- 이미 원격에 push한 커밋은 강제 `push(--force)`로만 덮을 수 있으나, **협업 때 조심**.
- 자동화 스크립트로 생성되는 파일들도 **스테이징 상태 꼼꼼히 다시 확인**해야 함!
- 커밋 리베이스나 암묵적으로 로그 `append`하는 자동화 도구는`reset` 이후에 재실행해도 안전.

---

## 📝 오늘 실제 경험 사례

```
# 같은 커밋 메시지를 두 번 커밋(중복) →
# 1. soft reset으로 중복 커밋을 내리고 작업물은 남기기

git reset --soft HEAD~2      # soft reset

# 혹은 git log --online -n 3   # 최근 3개까지 확인 안전하게 확인 후
# git reset --soft HEAD~2

# 2. git add
# a. 직접 하기 : git add <파일명1> <파일명2> ...
# b. 전체 : git add .
git add . 

# 3. Python 커밋 생성기 재실행 → 수정 커밋 메시지 새로 입력 → 단 1번만에 커밋 성공!
```

---

## 🔗 관련 문서

- [05_gitignore-log-structure.md](./05_gitignore-log-structure.md)
- [08_path-debug-case-study.md](./08_path-debug-case-study.md)

<br>

✅ 다음 문서 →  
📄 [07_cron-automation-howto.md](./07_cron-automation-howto.md): 크론/자동화/로그 스케줄러 실전 활용 노하우