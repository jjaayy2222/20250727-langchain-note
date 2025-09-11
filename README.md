# **`LangChain LLM Tutorial Practice Repository`**

## 개요 / Overview
- `../01/` ~ `../18/`: **"랭체인LangChain 노트 by 테디노트"** (Wikidocs: [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)) 책을 참고하여 진행하는 LLM(Large Language Model) 개발 연습을 위한 실습 프로젝트
  
- `../19/`, `../20/`: **"조코딩의 랭체인으로 AI 에이전트 서비스 만들기"** 책을 참고하여 진행하는 LLM(Large Language Model) 개발 연습을 위한 실습 프로젝트

  - `../19/`
    - 책의 내용을 따라가며 `LangChain 프레임워크를 활용한 LLM 연동` 및 `애플리케이션 개발` 기술을 `학습`하고 `실습`하는 데 중점
    - [`../19/README.me`](../20250727-langchain-note/19_LangChain-practice-basic/READEME.md) 참고

  - `../20/`
    - **LangChain** 을 활용한 **고급 실습** 을 다룸 → 여러 **에이전트**와 **도구**를 결합하여 복잡한 자동화 시스템과 고급 검색 시스템을 구축하는 방법 연습
    - [`../20/README.me`](../20250727-langchain-note/20_LangChain-practice-advanced/READEME.md) 참고

- This repository serves as an LLM development practice project, referencing the book **"LangChain Note by TeddyNote"** (Wikidocs: [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)) & **"Building an AI Agent Service with JoCoding's LangChain"** [조코딩의 랭체인으로 AI 에이전트 서비스 만들기](https://www.hanbit.co.kr/store/books/look.php?p_code=B8976154869).

- **주요 목적 / Main Purpose**
  - 책의 내용을 따라가며 LangChain 프레임워크를 활용한 LLM 연동 및 애플리케이션 개발 기술을 학습하고 실습하는 데 중점
  - The primary focus is on learning and practicing LLM integration and application development using the LangChain framework by following the book's content.

- **참고 사항 / Please Note**
  - 이 프로젝트는 **지속적으로 업데이트**될 예정입니다. 다만, 업데이트 일정은 명확하게 정해져 있지 않음
  - This project is subject to **ongoing updates**. However, there is no fixed update schedule.

  - 학습 과정에서 **참고하는 교재 및 다른 LLM 관련 예제의 내용과 다소 차이가 있을 수 있음.** 학습자의 환경(특정 API 설치 문제 등) 및 이해도에 따라 최적의 방법을 모색하거나, 특정 LLM API의 기능적/사용법적 특성을 고려하기 위함
  - During the learning process, there **may be slight deviations from the referenced book and other LLM-related examples.** This is done to explore optimal approaches based on the learner's environment (e.g., specific API installation issues) and understanding, or to account for the functional/usage characteristics of specific LLM APIs.

---

## 참고 / Reference
* [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [조코딩의 랭체인으로 AI 에이전트 서비스 만들기](https://www.hanbit.co.kr/store/books/look.php?p_code=B8976154869)
* [깃허브 저장소](https://github.com/sw-woo/hanbit-langchain/tree/main)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [OpenAI API Reference](https://platform.openai.com/docs/introduction)
* [**`Gen AI SDK`**](https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client) **참고**

---

## 프로젝트 개요 / Project Overview
* **핵심 프레임워크**: LangChain. LangGraph
* **LLM**: OpenAI, Google Gemini, Ollama 등
* **주요 도구**: LangSmith (추적 및 모니터링), python-dotenv (환경 변수 관리), pyenv/Poetry (Python 환경 관리) 등

---

## 🚩 프로젝트 진행 요약

> **📌 상세한 작업 이력 및 버전별 변경사항은 아래에서 확인 가능**  
> ➡️ [`docs/changelog/official.md`](./docs/changelog/official.md)


- ✅ 환경 구성 기본 완료: Python 3.13.5 + Poetry, pyenv 설정  
- ✅ LangSmith, Gemini API 연동 실험 및 설정 정리  
- ✅ LCEL(LangChain Expression Language) 학습 및 실행 구성  
- ✅ PromptTemplate 실습 코드 추가 및 병렬 실행 흐름 구현  
- ✅ 멀티모달 모델 기반 테스트 성공(Gemini streaming 등)

---

## 🛠 개발 환경 / Development Environment

- Python: 3.13.5 (via pyenv)
- Poetry: 의존성 관리 및 버전 고정
- 설치파일: `requirements.txt` → 지속 업데이트 중

---

## 📚 내부 문서 구조 / Documentation

해당 프로젝트는 실습/구현/분석 및 에러 대응 문서가 `/docs/` 아래 나뉘어 관리됩니다:

| 디렉토리 | 용도 요약 |
|----------|-----------|
| [`docs/concepts/`](./docs/concepts/) | LangChain 개념 설명, 내부 모듈 정리 |
| [`docs/papers/`](./docs/papers/) | 참고 논문 요약 & 정리자료 |
| [`docs/practice/`](./docs/practice/) | 실습 결과, 주요 코드 흐름 기록 예정 |
| [`docs/troubleshooting/`](./docs/troubleshooting/) | 에러 대응 및 문제 해결 자료 |
| [`docs/changelog/`](./docs/changelog/) | ✔️ 공식 업데이트 기록, 커밋 정리, 히스토리 트랙 |

<br>

## **🆕** 🚀 [**`인공지능 시인 App`**](https://ai-poet-with-gemini-flash-lite.streamlit.app/#b8c229c2) 배포 - `../19/02_ai-poet-creation/`

> • **📅 `updated`**: 2025.09.10.
>
> • **🔧 `Tech Stack`**: `gemini-2.5.-flash-lite` + `streamlit` + `python`

<br>

### 앱 배포 및 결과 화면

* 앱 실행 화면
<br>
![앱 실행 화면](../20250727-langchain-note/19_LangChain-practice-basic/02_ai-poet-creation/img/04_depolyment_1.png)

<br>

  * 시 생성 조건 입력 하기: `주제`, `스타일`, `참고 시인`
  <br>
    ![시 생성 조건 입력](../20250727-langchain-note/19_LangChain-practice-basic/02_ai-poet-creation/img/04_depolyment_4.png)

<br>

* 시 생성 결과 화면
<br>
![시 생성 결과](../20250727-langchain-note/19_LangChain-practice-basic/02_ai-poet-creation/img/04_depolyment_5.png)

<br>

### 관련 문서 위치
 
* `19_LangChain-practice-basic/02_ai-poet-creation/` - 실습 파일 폴더

* `docs/practice/deploymen/` - 실습 과정 및 결과 정리

* `docs/troubleshooting/Streamlit-deployment-gemini-api-timeout.md` / `docs/troubleshooting/Streamlit-deployment-gemini-api-timeout.pdf` - 배표과정 트러블슈팅 정리


<br>

---

## 🛠️ Git 커밋 메시지 자동 생성기(`gen_langchain_commit.py`)

본 프로젝트에서는 커밋 로그 작성의 일관성과 기록 관리를 위한 **Python 기반의 CLI 커밋 메시지 생성기를 함께 제공**

- 기능
  - 커밋 타입 선택 (`feat`, `fix`, `docs` 등)
  - prefix[#버전] 자동 추천 (예: `#13.6` → `#13.7`)
  - `git diff` 기반 변경 파일 안내
  - 제목 및 본문 입력 (멀티라인 가능)
  - 최종 커밋 메시지 미리보기 기능
  - 커밋 후, `docs/changelog/py-gen-langchain-commit-log.md`에 자동 백업

- 목적
  - 커밋 히스토리 자동 백업 (수동 changelog와는 별도)
  - 커밋 메시지 생성기의 출력 내역을 보존
  - 운영 중 불가피한 커밋 유실을 대비한 참고용 로그

📁 위치: `scripts/gen_langchain_commit.py`

📁 **자동 로그 파일 경로**: `docs/changelog/py-gen-langchain-commit-log.md`

📄 공식 릴리즈 정보 `changelog` → `docs/changelog/official.md` 참조

📄 수동 요약 `changelog` ➡︎ `docs/changelog/commit-log.md` 참조

🎯 실행 방법:

```bash
python scripts/gen_langchain_commit.py
```

또는

```bash
./scripts/gen_langchain_commit.py
```

---

📌 이 프로젝트는 계속 업데이트되고 있습니다.  