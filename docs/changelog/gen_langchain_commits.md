# 🛠️ Git 커밋 메시지 자동 생성기 (gen_langchain_commit)

LangChain 노트 프로젝트의 커밋 메시지를 구조적이고 일관되게 관리하고,  
기록 실수 없이 자동으로 docs/changelog에 로그를 남기기 위한 CLI 커밋 도우미입니다.

> 🗂 관련 파일:  
> - `scripts/gen_langchain_commit.py`  
> - [자동 로그 백업 스크립트](extract_langchain_commits.sh)

## ✨ 기능 요약

| 기능                             | 설명 |
|----------------------------------|------|
| ✅ 타입(prefix) 선택 UI           | 커밋 타입(feat, fix, docs 등)을 번호로 선택 가능 |
| ✅ prefix 번호 자동 증가 제안     | 이전 커밋의 prefix (예: #13.6) → 자동으로 #13.7 추천 |
| ✅ 최근 입력값 자동 기억 (캐싱)   | 최근 사용한 타입, 번호, 제목을 기본값으로 미리 채워줌 |
| ✅ 제목/본문 분리 입력 지원       | 제목은 한 줄 / 본문은 여러 줄 입력 지원 (빈 줄 엔터로 종료) |
| ✅ 변경된 파일(diff) 미리 보기   | 커밋 전 현재 변경된 파일 목록 출력 (git diff --name-only) |
| ✅ 최종 메시지 미리보기 (Dry-Run) | 커밋 전 최종 메시지를 보여주고 승인 여부 확인 |
| ✅ git add . → commit 자동화     | 입력 완료 후 커밋 실행까지 자동 처리 |
| ✅ docs에 커밋 메시지 자동 기록   | `docs/changelog/commit-log.md`에 자동 append |

## 📄 사용 방법 (Python CLI 실행)

```bash
python scripts/gen_langchain_commit.py
# 또는
./scripts/gen_langchain_commit.py
```

> 첫 실행 시 실행 권한이 없다면 아래 명령으로 추가:

```bash
chmod +x scripts/gen_langchain_commit.py
```

## 🧪 사용 예시 흐름

```text
📝 변경된 파일:
  · README.md
  · gen_langchain_commit.py
──────────────────────────────

커밋 타입:
1) feat  2) fix  3) docs  4) chore  5) refactor  6) build
번호 선택 (Enter=1): 3
prefix[#번호] (Enter=13.7): 
커밋 제목 (Enter=문서 자동 생성기 문서화): 커밋 자동화 기록 작성
커밋 본문 (빈 줄 입력 시 종료):
기능 요약, 실행법, 주요 항목 정리 완료
상세 기능 옵션은 추후 버전에 반영 예정

🧾 최종 메시지:
========================================
docs[#13.7]: 커밋 자동화 기록 작성

기능 요약, 실행법, 주요 항목 정리 완료
상세 기능 옵션은 추후 버전에 반영 예정
========================================

✅ 이 메시지로 git add + commit 하시겠어요? (y/n): y
```

## 📁 결과

- 커밋 수행됨 → `git commit -m "...."`
- message가 `/docs/changelog/commit-log.md` 맨 아래에 자동 append됨

## 🔄 내부 구성 요소

| 파일 | 설명 |
|------|------|
| `gen_langchain_commit.py` | 실제 Python 기반 CLI 생성기 |
| `gen_langchain_commit_cache.json` | 마지막 입력 내용을 저장하는 캐시 데이터 |
| `commit-log.md` | 커밋 로그 백업 append 대상 파일 |

## 📌 향후 추가될 수 있는 기능 아이디어

- [ ] prefix 버전단위(13.x → 14.0) 자동 제안
- [ ] 특정 파일/폴더에 따라 커밋 타입 자동 지정 (`src/ → feat`, `README.md → docs`)
- [ ] `--dry` 모드 / 실제 커밋 없이 메시지 출력만
- [ ] more emoji-extended preset 🎉

