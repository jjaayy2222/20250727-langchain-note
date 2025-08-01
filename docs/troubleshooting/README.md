# 🧭 Troubleshooting 폴더 소개

이 폴더는 본 프로젝트를 진행하면서 발생했던 문제 상황, 오류 이슈, 환경 설정 실패 등의 트러블슈팅 기록을 정리한 공간입니다.

프로젝트 환경은 LangChain, pyenv, Gemini API, VSCode 기반의 Python 개발 환경을 기반으로 하며,  
여기에는 다음과 같은 항목들이 포함됩니다:

- 시스템 설정 문제 및 해결 (예: VSCode CLI, `code` 명령어 인식 오류 등)
- Python 가상환경(pyenv) 관련 충돌
- LangChain 도구 설정 및 실행 오류
- 패키지 의존성 문제, 환경 변수 충돌
- Shell 설정(zsh 등) 문제가 작업에 영향을 준 경우

---

## 📄 작성 규칙

**템플릿은 [`_template.md`](./_template.md) 참고**

모든 문서는 아래와 같은 항목을 포함하는 것을 권장합니다:

- ❗️ 문제 상황 요약
- 🔍 원인 분석
- 🧪 시도한 방법 (실패 포함)
- ✅ 최종 해결법
- 💬 참고/교훈
- 📌 환경 정보 (OS, 터미널, Python 등)

---

## 💡 정리 팁

- 서술형/연대기순보다, **이슈별, 테마별**로 구분 저장 권장
- 완전히 다른 문제 성격이라면 새로운 `.md` 파일로 분리
- 파일 이름은 `명사형 + kebab-case` 권장:
  - 예시:
    - `vscode-path-error.md`
    - `jupyter-kernel-missing.md`
    - `pyenv-shell-init-issue.md`
- 반복 이슈는 같은 파일 내에 날짜/구분 섹션으로 추적 
  - 예시 : `## [2025-08-01]`

---

## 📋 폴더 내 문서 인덱스

- [Troubleshooting 폴더 소개](./README.md)
- [Troubleshooting 템플릿](./_template.md)
- [VSCode 편집기 설정 문제](./vscode-fetch-error.md)

---

## 🏷️ 하위 문제 파일 태그 기준

각 문제 문서의 **맨 앞 또는 맨 뒤**에 아래와 같이 태그(키워드)를 달아주면,
- 검색, 필터, 문서 자동 인덱싱, MkDocs advanced search, wiki 등에서 효율적으로 관리 가능

```
---
tags:
  - vscode
  - shell
  - path
  - macos
  - cli
  - 환경설정
---
```
> **주요 태그 분류 예시**  
> - os: macos, windows, linux  
> - 도구/라이브러리: vscode, pyenv, jupyter, langchain, poetry  
> - 이슈 유형: path, permission, 설치, 환경변수, 권한, 설정오류  
> - 작업군: 프로젝트설정, 환경관리, 실행오류, 패키지, 커밋

* 태그는 자유롭게 조합 가능

---

## ⚙️ MkDocs 연동 & 자동 인덱스/검색

- MkDocs(project docs/static site 생성기) 연동시, `docs/troubleshooting/` 폴더 내 `*.md` 파일이 자동 탐색·출력됨
- `mkdocs.yml`에 아래처럼 추가:

```
nav:
  - 개요: index.md
  - 트러블슈팅:
      - VSCode 문제: troubleshooting/vscode-path-error.md
      - Jupyter 문제: troubleshooting/jupyter-kernel-missing.md
      - ...다양한 이슈
```

- **MkDocs 플러그인 예시**:
    - `awesome-pages-plugin`: 폴더별 자동 인덱싱/정렬 지원
    - `tags-plugin`: 태그 기반 자동 분류/검색 지원
    - `search` 플러그인: 키워드/태그 연계 검색 강화

자세한 설정은 `mkdocs.yml`, 그리고 공식 [MkDocs docs](https://www.mkdocs.org/user-guide/writing-your-docs/) 참조

---

## 💡 TIP

- 모든 이슈 기록 시 반드시 **태그** 부여 습관화 (ex. `tags: [vscode, shell, path, macos]`)
- 폴더 내 `README.md`는 반드시 인트로/분류/가이드 역할로 유지
- 템플릿(`_template.md`)은 항상 최신화
- 문서 대량 추가시, MkDocs rebuild 후 인덱스·검색 확인

---

이 폴더는 장기적으로 팀 또는 개인의 성장 자산이자,  
같은 문제 재발 시 시간을 크게 절약할 수 있는 "문제 해결 기록 저장소"로 활용됩니다. 💾

> 편하게 기록하세요. 완벽보다 중요한 건 남기는 것입니다. ✍️

```

### 🔧 저장 위치 제안

```
docs/
└── troubleshooting/
    ├── README.md                ← ✅ 위 내용 저장
    ├── _template.md             ← 🔧 템플릿 참고용
    ├── vscode-path-error.md     ← 🔧 vscode-fetch-error 기록
    └── [...추가되는 issue들]
```
