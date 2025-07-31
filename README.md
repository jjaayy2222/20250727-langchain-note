# 20250727-langchain-llm-tutorial (LangChain LLM Tutorial Practice Repository)

- 이 저장소는 **"랭체인LangChain 노트 by 테디노트"** (Wikidocs: [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)) 책을 참고하여 진행하는 LLM(Large Language Model) 개발 연습을 위한 실습 프로젝트
- This repository serves as an LLM development practice project, referencing the book **"LangChain Note by TeddyNote"** (Wikidocs: [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)).

**주요 목적 / Main Purpose**
- 책의 내용을 따라가며 LangChain 프레임워크를 활용한 LLM 연동 및 애플리케이션 개발 기술을 학습하고 실습하는 데 중점
- The primary focus is on learning and practicing LLM integration and application development using the LangChain framework by following the book's content.

**참고 사항 / Please Note**
* 이 프로젝트는 **지속적으로 업데이트**될 예정입니다. 다만, 업데이트 일정은 명확하게 정해져 있지 않음
* This project is subject to **ongoing updates**. However, there is no fixed update schedule.

* 학습 과정에서 **참고하는 교재 및 다른 LLM 관련 예제의 내용과 다소 차이가 있을 수 있습니다.** 이는 학습자의 환경(특정 API 설치 문제 등) 및 이해도에 따라 최적의 방법을 모색하거나, 특정 LLM API의 기능적/사용법적 특성을 고려하기 위함
* During the learning process, there **may be slight deviations from the referenced book and other LLM-related examples.** This is done to explore optimal approaches based on the learner's environment (e.g., specific API installation issues) and understanding, or to account for the functional/usage characteristics of specific LLM APIs.

---

## 참고 / Reference
* [랭체인LangChain 노트 by 테디노트](https://wikidocs.net/book/14314)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [OpenAI API Reference](https://platform.openai.com/docs/introduction)
* **[`Gen AI SDK`]** (https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client) **참고**

---

## 프로젝트 개요 / Project Overview
* **핵심 프레임워크**: LangChain. LangGraph
* **LLM**: OpenAI, Google Gemini, Ollama 등
* **주요 도구**: LangSmith (추적 및 모니터링), python-dotenv (환경 변수 관리), pyenv/Poetry (Python 환경 관리) 등

---

## 진행 상황 / Current Progress
-   초기 개발 환경 설정 완료 (Python, Poetry, 가상 환경 관리)
-   LangSmith API 연동 및 프로젝트 추적 기능 설정 완료
-   Gemini API LangChain 연동 및 주요 기능
-   Google Gemini API 연동 시도
    - 제미나이 버전으로 시도 중
    - 라이브러리 설치 및 API 사용법 관련 일부 문제 발생 -> 해결
    - **멀티모달 모델(이미지 인식, 스트리밍) 성공**
    - **시스템, 유저 프롬프트 성공**
- 개발 환경 재설정
    - 개발 환경 의존성 -> 충돌 문제 -> 파이썬 재설치 및 requirments.txt 재정비
    - 파이썬: `pyenv` 설정 반영을 위한 `.python-version` 업데이트
- Gemini 멀티모달 스트리밍 기능 구현 및 테스트 성공
    - `02-Gemini-LLM.ipynb` 실행 전 test 진행: 01_basic/01_2_GEMINI_TEST
    - `test_cell_outputs.md`: `test2.py`, `test_gemini.py` 테스트 결과 정리
    - `test_gemini_prompt.py` -> 프롬프트 수정 연습 및 성공 -> `test_gemini_prompt_cell_ouputs.md`에 테스트 결과 정리 및 저장**
- LCEL
    - LangChain Expression Language 개념
    - 기본 구성 : 프롬프트(템플릿 활용) + 모델 + 아웃 파서
    - `stream`, `invoke`
- LCEL interface
    - 표준 인터페이스**: `stream`, `invoke`, `batch`
    - 비동기 메소드: `astream`, `ainvoke`, `abatch`, `astream_log`
    - Runnable: `RunnablePassthrough`, `RunnablePassthrough()`, `RunnablePassthrough.assign(...)`, `RunnableLambda`, `operator.itemgetter`
- **`Prompts`**
    - **`Prompt`**
      - **`PromptTemplate`: `from_template()`, `PromptTemplate`객체 생성으로 프롬프트 생성, `partial_variables`, `파일로부터 template 읽어오기`, `ChatPromptTemplate`, `MessagePlaceholder`**

---

**개발 환경 / Development Environment:**
-   **Python**: Python 3.13.5 (pyenv를 통해 관리)
-   **Poetry**: 프로젝트 의존성 관리 도구
-   **세부 의존성 -> 현재 수정 중**
-   **설치 환경**: `requirements.txt`에서 확인 가능, 계속 업데이트 예정

---

**📚 Documentation**

- **[`docs/`](./docs/)**: 이 프로젝트의 관련 문서 정리
  - [`concepts/`](./docs/concepts/)
      - 프로젝트 관련 핵심 개념과 이론적 배경
      - 새로운 기능을 개발하거나 프로젝트의 근간을 이해하는 데 필요한 정보 포함
  -  **[`papers/`](./docs/papers/)**
     -  프로젝트와 관련된 **논문이나 연구 자료**
     -  해당 논문에 대한 요약 및 핵심 내용 정리 
           -  ➡️ **[goole_prompt_guide_summary/](./docs/papers/google_prompt_guide_summary/)**생성
           -  ➡️ **프롬프트 학습 전 최신 공식 가이드 숙지 및 요약, 정리, 공유**
  - [`practice/`](.docs/practice/)
    - 프로젝트 개발 과정에서의 실습 결과, 구현 과정, 주요 결정 사항 등을 기록 예정 
    - 실제 코드와 연계된 설명 예정
  - [`troubleshooting/`](./docs/troubleshooting/)
    - 개발 중 발생했던 **주요 에러와 해결 방법** 정리 예정
