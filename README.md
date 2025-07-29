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
- **Gemini 멀티모달 스트리밍 기능 구현 및 테스트 성공**
    - **`Gen AI SDK` [https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client] 참고**
    - `02-Gemini-LLM.ipynb` 실행 전 test 진행: 01_basic/01_2_GEMINI_TEST
    - `test_cell_outputs.md`: `test2.py`, `test_gemini.py` 테스트 결과 정리
    - **`test_gemini_prompt.py` -> 프롬프트 수정 연습 및 성공 -> `test_gemini_prompt_cell_ouputs.md`에 테스트 결과 정리 및 저장**

---

**개발 환경 / Development Environment:**
-   **Python**: Python 3.13.5 (pyenv를 통해 관리)
-   **Poetry**: 프로젝트 의존성 관리 도구
-   **세부 의존성 -> 현재 수정 중**
-   **설치 환경**: `requirements.txt`에서 확인 가능, 계속 업데이트 예정

---