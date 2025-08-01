# 🧾 커밋 메시지 로그 (Persistent Commit Message Log)

* 해당 로그는 특정 날짜 또는 히스토리 재정비 이전/이후의 커밋 메시지를 백업하며,  
이력이 날아갈 경우를 대비하거나 회고, 릴리즈 추출용으로 사용됩니다.

* 이 문서는 깃 히스토리를 수동으로 백업하는 용도로 작성되며,  
git rebase, squash, reset, force-push 등으로 발생할 수 있는 메시지 유실에 대비한 스냅샷입니다.

---

## 📆 2025-08-01

- [`773ac99`] **docs[#13.1]: 프로젝트 소개 정비 및 changelog 링크 추가**
    - `README.md` 내 진행상황/구조 요약을 정리
    - 상세 진행 내역은 `changelog`로 이동, 공식 링크 추가
    - 문서 구조 테이블 및 주요 참고 링크 보완
- ['6d63c61'] **docs[#13.4]: 커밋 메시지 복구 및 rebase 히스토리 트러블슈팅 기록 추가**
    - `lost-found` 대상 커밋 메시지 복원 흐름 정리
    - `fsck`, `--allow-empty`, `rebase -i` 사용 과정 정리
    - 향후 메시지 유실/복구 대응을 위한 기준 문서 생성
- [`a70d654`] **build[#13.3]: 문서 사이트 구성을 위한 mkdocs 설정 및 인덱스 문서 추가**    
    - `mkdocs.yml`: 문서 사이트 설정 초기화
    - `docs/index.md`: 프로젝트 소개 및 구조 개요 문서 추가
- [`dc258f7`] **docs[#13.2]: changelog 문서 및 커밋 이력 기록 추가**
    - `official.md`: 버전별 업데이트 로그 정리
    - `commit-log.md`: 커밋 메시지 스냅샷 수동 백업
    - `2025-08-01-rebase-track.md`: rebase 및 메시지 복구 이력 정리
- [`dc258f7`] **docs[#13.1]: 프로젝트 소개 정비 및 changelog 링크 추가** → 충돌 → 병합 후 재커밋
    - `README.md` 내 진행상황/구조 요약을 정리
    - 상세 진행 내역은 `changelog`로 이동, 공식 링크 추가
    - 문서 구조 테이블 및 주요 참고 링크 보완
- [`9c0b164`] Merge branch `restore`

    ---

- `rebased`
  - [`6936e76`] feat[#5]: Runnable 실습 및 체인 구조 정리, 프롬프트 개선 학습 기록
  - [`960d24c`] feat[#12.2]: LangChain 프롬프트 템플릿 실습 코드 및 문서 보완
  - [`a2d1420`] feat[#12.1]: 문서 구조 추가 및 초기 문서 내용 반영
  - [`a90d10b`] feat[#11]: Runnable 체인 구조 학습 정리
  - [`1c19ff8`] feat[#10.4]: LCEL 학습 및 README 업데이트
  - [`1dea3c2`] fix[#10.3]: Gemini-LLM.ipynb 오타 수정
  - [`7c06ec5`] docs[#10.2]: Jupyter 셀 정리 및 이미지 보완
  - [`2071b57`] feat[#10.1]: 재무제표 멀티모달 예제 및 프롬프트 최적화
  - [`40087ac`] feat[#9.2]: Gemini 스트리밍 테스트 및 샘플 구현
  - [`1479cc1`] refactor[#9.1]: Python 환경 및 의존성 구조 변경

---

## 📆 2025-07-27

- [`4bbe5be`] feat[#1]: 초기 LangChain 프로젝트 설정 완료
