# 🔧 Git 커밋 메시지 손실 및 rebase 정비 과정
작성일: 2025-08-01  
작성자: jjaayy2222

## 🧨 문제 상황

- 커밋 메시지를 정성 들여 작성해서 push 했으나,  
  중간 일부 커밋 메시지 구간(#2 ~ #8)이 깃 로그 및 히스토리에서 사라진 상태
- 메인 브랜치에서 일부 커밋이 사라진 것처럼 보여 멘붕 🤯

> **작성 목적:**  
- 깃 커밋 메시지 일부가 사라졌고, fsck로 일부 복구했으며,  
- 그 커밋 메시지만 복원하고 전체히스토리 rebase로 다시 정리했다는 과정 기록  
- 향후 다시 rebase 할 때 참고할 수 있는 내용과 전략도 함께 명시

## 🔍 원인 분석

- `git rebase`, `commit --amend`, `reset`, `stash` 등의 반복 작업 후  
  브랜치 간 커밋 이력이 교차되며 일부 커밋 이력이 분기에서 단절됨
- 그 결과 → 과거 브랜치에서 나온 커밋들은 orphan(dangling) 커밋이 되었고,  
  Git은 더 이상 main 브랜치에서 참조하지 않게 됨
- 일부는 GC에 의해 완전 삭제됨

## 🛠 조치 계획 및 흐름

1. `git fsck --unreachable` / `git fsck --lost-found` 로 dangling 커밋 확인
2. `git show <해시>`로 커밋 메시지 복원 가능성 확인
3. 복구 가능한 메시지를 `--allow-empty` 커밋으로 restore 브랜치에 저장
4. 전체 커밋 정비를 위해 `git rebase -i HEAD~10` 실행
5. 커밋 메시지 일괄 정리 (pick → reword)
6. 정리 완료된 restore 브랜치를 main 브랜치에 merge 예정

## 📝 복구한 커밋 메시지

```
feat(Runnable): Runnable 실습 및 체인 구조 정리, 프롬프트 개선 학습 기록_#5

- batch, invoke 실험 기록 및 출력 비교
- 체인 구조 흐름 정리 (Lambda, Parallel, Passthrough 등)
- AIMessage 출력 구조 정리 및 기능 분류
- original missing commit: 3bd1db9
```

## 📌 트러블슈팅 요약 (`if rebase` 하게 될 때)

- 커밋 메시지 사라짐 원인: rebase or reset 후 GC 처리
- `git fsck`는 `--unreachable`, `--lost-found` 모두 확인
- `git show` → 메시지만 복사해 .md로 남기자!
- 메시지를 다시 커밋하려면?  
  👉 `git commit --allow-empty -m "복구 메시지"`

---
<br>
📦 브랜치: `restore`  

🎯 다음 단계: `main`에 `merge` or `rebase 후 push`!

---