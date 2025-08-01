# 🧾 공식 커밋 히스토리 / 주요 릴리즈 변경 로그 (Official Changelog)

※ 이 문서는 기능 단위 milestone을 기준으로 프로젝트의 주요 커밋 흐름을 요약한 공식 changelog입니다.  
→ 📘 날짜별 상세 커밋 메시지는 commit-log.md 참고

---

## 📦 #14 커밋 메시지 자동 생성 시스템 도입 (2025-08-01)

- 🛠 Python 기반 CLI 툴 `gen_langchain_commit.py` 개발 완료
    - 커밋 타입 선택 (feat, fix, docs 등)
    - prefix 자동 증가 제안 (#13.6 → #13.7 등)
    - 멀티라인 제목/본문 분리 입력
    - 파일 변경내역 안내: git diff --name-only
    - 커밋 메시지 Dry-run (미리보기 → 커밋 여부 선택)
    - 최근 커밋 입력값 타입/번호/제목 캐싱
- 📝 커밋 확정 후 자동으로 `docs/changelog/commit-log.md`에 메시지 append 처리
- 📄 실행용 스크립트 구성:
    - scripts/gen_langchain_commit.py
    - scripts/gen_langchain_commits.md (사용법/기능 정리 문서)
- 🌟 향후 확장 예정:
    - 커밋 타입 자동 감지
    - prefix 버전 단위 자동 증가
    - 커밋 메시지 push hook 연동
    - GitHub PR/issue 자동 링크 생성 등

---

## 📦 #13 커밋 복구 및 히스토리 리베이스 대응 (2025-08-01)

- 🔄 Git 리베이스 과정 중 커밋 메시지 유실 → fsck 기반 복구
    - git fsck --lost-found → 유실 해시 확인
    - git show {해시} → 메시지 복원
    - git commit --allow-empty, rebase -i 흐름 구조화
- 📁 문서화 구성:
    - commit-log.md: 커밋 메시지 백업
    - rebase-track.md: 리베이스 작업 및 문제해결 흐름
    - official.md: milestone 단위 버전 정리
- 💡 장기 커밋 기록 보존을 위한 markdown 기록 기반 구축

---

## 📦 #12 LangChain 프롬프트 템플릿 실습 정리 (2025-07-30)

- 💬 LangChain PromptTemplate / ChatPromptTemplate 실사용 코드 구성
    - from_template, partial_parameters, 대화형 PromptTemplate 실험
    - 프롬프트 로딩, YAML 기반 템플릿 저장 실습
- 📄 문서화:
    - 02_Prompt/01_PromptTemplate.ipynb
    - docs/concepts/ 디렉토리 내 프롬프트 설명 보완

---

## 📦 #11 Runnable 체인 구조 학습 및 LCEL 실습 (2025-07-30)

- 🧠 LangChain Expression Language + Runnable 계열 학습
    - RunnableLambda, RunnableParallel, batch, ainvoke 등 흐름 학습
    - Few-shot Prompt 구성 → 실행 흐름 기록
- 📁 주요 파일:
    - 04_LCEL_Advanced.ipynb
    - 05_Runnable.ipynb
- 📗 문서화 및 정리 진행:
    - AIMessage.content 출력 구조 분석
    - invoke → 병렬 후처리 체인 구성 흐름 구분

---

📌 향후 milestone changelog는 위 구조를 따라 추가 작성하도록 합니다.
📎 관련 문서:
- README.md — 전체 시스템 개요 및 스크립트 실행법 안내
- commit-log.md — 날짜별 커밋 메시지 snapshot
- gen_langchain_commits.md — 자동 커밋 생성 도구 기능/사용법 안내
