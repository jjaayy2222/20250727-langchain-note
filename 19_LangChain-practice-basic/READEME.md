# 19_LangChian-practice-basic

- 이 저장소는 **"조코딩의 랭체인으로 AI 에이전트 서비스 만들기"** (해당 깃허브 저장소: [실습 예제 코드](https://github.com/sw-woo/hanbit-langchain/tree/main)) 책을 참고하여 진행하는 LLM(Large Language Model) 개발 연습을 위한 실습 프로젝트


**주요 목적 / Main Purpose**
- 책의 내용을 따라가며 LangChain 프레임워크를 활용한 LLM 연동 및 애플리케이션 개발 기술을 학습하고 실습하는 데 중점

**참고 사항 / Please Note**
* 이 프로젝트는 **지속적으로 업데이트**될 예정. 다만, 업데이트 일정은 명확하게 정해져 있지 않음
* This project is subject to **ongoing updates**. However, there is no fixed update schedule.

* 학습 과정에서 **참고하는 교재 및 다른 LLM 관련 예제의 내용과 다소 차이가 있을 수 있음.** 이는 학습자의 환경(특정 API 설치 문제 등) 및 이해도에 따라 최적의 방법을 모색하거나, 특정 LLM API의 기능적/사용법적 특성을 고려하기 위함

---

## 참고 / Reference
* [조코딩의 랭체인으로 AI 에이전트 서비스 만들기](https://www.hanbit.co.kr/store/books/look.php?p_code=B8976154869)
* [깃허브 저장소](https://github.com/sw-woo/hanbit-langchain/tree/main)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [OpenAI API Reference](https://platform.openai.com/docs/introduction)
* **[`Gen AI SDK`]** (https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client) **참고**

---

## 프로젝트 개요 / Project Overview
* **핵심 프레임워크**: `LangChain`, `LangGraph`
* **LLM**: `OpenAI`, `Google Gemini`, `Ollama` 등
* **주요 도구**: `LangSmith` (추적 및 모니터링), `python-dotenv` (환경 변수 관리), `pyenv`/`Poetry` (Python 환경 관리) 등

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

해당 프로젝트는 실습/구현/분석 및 에러 대응 문서가 `/docs/` 아래 나뉘어 관리:

| 디렉토리 | 용도 요약 |
|----------|-----------|
| [`docs/concepts/`](./docs/concepts/) | LangChain 개념 설명, 내부 모듈 정리 |
| [`docs/papers/`](./docs/papers/) | 참고 논문 요약 & 정리자료 |
| [`docs/practice/`](./docs/practice/) | 실습 결과, 주요 코드 흐름 기록 예정 |
| [`docs/troubleshooting/`](./docs/troubleshooting/) | 에러 대응 및 문제 해결 자료 |
| [`docs/changelog/`](./docs/changelog/) | ✔️ 공식 업데이트 기록, 커밋 정리, 히스토리 트랙 |

---

## 📂 **폴더 구조 예시**:

```plaintext
../19_LangChain-practice-basic
    │
    ├── 01_ReviewAI
    │   ├── 01_food-review-ai
    │   ├── 02_restaurant-review-ai
    │   └── 03_lcel-accommodation-review-ai
    │
    └── 02_ai-poet-creation
        ├── 01_llm-chain-creation
        ├── 02_app-deployment
        └── 03_streamlit-usage
```

### **`01_ReviewAI`**

* 내용: **PromptTemplate**을 활용하여 프롬프트를 효율적으로 관리하고, 텍스트 생성에 대한 실습을 다룬 예제

* 주요 내용:
  * **프롬프트 템플릿**을 활용하여 더 효율적인 텍스트 생성을 다룬 예제
  * **기본적인 LLM 활용**: 프롬프트 설계와 템플릿을 통해 더 효율적으로 처리하는 방법 연습

<br>

### **`02_ai-poet-creation`**

* 내용: `LangChain`의 **`에이전트 기능`** 을 소개하고, 이를 활용한 기본적인 예제

* 주요 내용:
  * **`Agent`의 사용법**과 기본적인 응용 연습
    * 예시: 단일 에이전트를 활용한 `간단한 자동화`
  * **`Agent`의 행동 흐름 제어**: 에이전트를 어떻게 제어하고, 이를 통해 더욱 복잡한 작업을 자동화할 수 있는 방법 연습

<br>

---

## 참고 / Reference
* [조코딩의 랭체인으로 AI 에이전트 서비스 만들기](https://www.hanbit.co.kr/store/books/look.php?p_code=B8976154869)
* [깃허브 저장소](https://github.com/sw-woo/hanbit-langchain/tree/main)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [OpenAI API Reference](https://platform.openai.com/docs/introduction)
* **[`Gen AI SDK`]** (https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client) **참고**

---

📌 이 프로젝트는 계속 업데이트되고 있습니다.  
업데이트 로그는 👉 [`./docs/changelog/official.md`](./docs/changelog/official.md)에서 확인