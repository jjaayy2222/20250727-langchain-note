# 20_LangChain-practice-advanced

## 개요

- 이 저장소는 **"조코딩의 랭체인으로 AI 에이전트 서비스 만들기"** (해당 깃허브 저장소: [실습 예제 코드](https://github.com/sw-woo/hanbit-langchain/tree/main)) 책을 참고하여 진행하는 LLM(Large Language Model) 개발 연습을 위한 실습 프로젝트
- 이 프로젝트는 **LangChain**을 활용한 고급 실습을 다룸
- 여러 **에이전트**와 **도구**를 결합하여 복잡한 자동화 시스템과 고급 검색 시스템을 구축하는 방법 연습 


## 주요 목적
- 책의 내용을 따라가며 LangChain 프레임워크를 활용한 LLM 연동 및 애플리케이션 개발 기술을 학습하고 실습하는 데 중점
- **멀티모달 데이터**와 **고급 RAG** 기법을 활용한 다양한 서비스 구현 예시 연습에 중점

## 참고 사항
* 이 프로젝트는 **지속적으로 업데이트**될 예정. 다만, 업데이트 일정은 명확하게 정해져 있지 않음

* 학습 과정에서 **참고하는 교재 및 다른 LLM 관련 예제의 내용과 다소 차이가 있을 수 있음.** 이는 학습자의 환경(특정 API 설치 문제 등) 및 이해도에 따라 최적의 방법을 모색하거나, 특정 LLM API의 기능적/사용법적 특성을 고려하기 위함

---

## 참고
* [조코딩의 랭체인으로 AI 에이전트 서비스 만들기](https://www.hanbit.co.kr/store/books/look.php?p_code=B8976154869)
* [깃허브 저장소](https://github.com/sw-woo/hanbit-langchain/tree/main)
* [LangChain 공식 Document](https://www.langchain.com/docs/)
* [OpenAI API Reference](https://platform.openai.com/docs/introduction)
* **[`Gen AI SDK`]** (https://ai.google.dev/gemini-api/docs/migrate?hl=ko#client) **참고**

---

## 주요 스택
* **핵심 프레임워크**: `LangChain`, `LangGraph`
* **LLM**: `OpenAI`, `Google Gemini`, `Ollama` 등
* **주요 도구**: `LangSmith` (추적 및 모니터링), `python-dotenv` (환경 변수 관리), `pyenv`/`Poetry` (Python 환경 관리) 등

---

## 🚩 프로젝트 진행 요약

> **📌 상세한 작업 이력 및 버전별 변경사항은 아래에서 확인 가능**  
> 
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
../20_LangChain-practice-advanced
    ├── 01_Multilingual-Email-Generator
    ├── 02_Chat-PDF-Generator
    ├── 03_Create-Bot-Author-Hyeon-Jin-geon
    ├── 04_RAG-Similarity-Search-Service
    │   ├── 001_FAISS-Index-Creation
    │   ├── 002_FAISS-Vector-DB-Similarity-Search
    │   └── 003_RAG-Based-Large-Scale-Text-Search
    ├── 05_Advanced-RAG-News-Search-Service
    │   ├── 001_Multiquery-News-Search-System
    │   └── 002_Hybrid-Search-System
    ├── 06_Integrated-Service-Using-Multimodal-Data
    │   ├── 001_Multimodal-Data-RAG-System
    │   ├── 002_FashionRAG-Image-Styling-Assistant
    │   └── 003_Poetry-Novel-Generation-Service
    ├── 07_Agent-Systems-LangGraph-Agentic-RAG
    │   ├── 001_AI-Agent-Using-Tools
    │   ├── 002_AI-Agent-Using-LangGraph
    │   └── 003_Intelligent-Information-Search-Agentic-RAG
    └── 08_Collaborative-Agent-System-Crew-AI
        ├── 001_Multi-Agent-Blog-Writing-System
        ├── 002_Blog-Content-Generator-FastAPI-CrewAPI
        └── 003_Complete-Blog-Service-With-React-Integration
```

### **`05. 고급 RAG 기법을 활용한 뉴스 검색 서비스`**

* 내용: 
  * **고급 RAG 기법**을 사용하여 **뉴스 검색** 시스템 구현
  * 사용자가 입력한 여러 쿼리 조건을 기반으로 최적의 뉴스 기사를 검색하는 시스템을 만들기

* 주요 내용:
  * **Multiquery 기반 뉴스 검색 시스템**: 여러 쿼리를 기반으로 효율적인 뉴스 검색 구현
  * **하이브리드 검색 시스템**: 검색 결과를 더 정확하게 제공하기 위해 **하이브리드 검색 시스템**을 활용

<br>

### 06. **`멀티모달 데이터를 활용한 통합형 서비스`**

* 내용:
  * **멀티모달 데이터**를 활용하여 다양한 형태의 정보를 통합하는 서비스
  * **`텍스트`, `이미지`, `비디오` 등 다양한 데이터 소스를 통합** → 더 나은 사용자 경험을 제공

* 주요 내용:
  * **멀티모달 데이터 RAG 시스템 만들기**: 텍스트와 이미지를 결합한 검색 시스템 구현
  * **FashionRAG: 이미지 기반 스타일링 어시스턴트**: 이미지 기반으로 사용자의 스타일을 분석하고 추천하는 시스템
  * **시, 소설 생성 서비스 만들기**: 텍스트 생성 AI를 활용하여 시와 소설을 생성하는 서비스 구현

<br>

### 07. **`랭그래프와 Agentic RAG를 활용한 에이전트`**

* 내용: **랭그래프**와 **Agentic RAG**를 활용하여 복잡한 정보 검색 시스템을 구축하는 **AI 에이전트** 만들기

* 주요 내용:
  * **도구를 활용하는 AI 에이전트**: 다양한 도구를 활용하여 정보 처리 및 작업 자동화.
  * **랭그래프를 활용한 AI 에이전트**: 랭그래프 기법을 사용하여 정보의 관계를 파악하고 작업을 수행하는 에이전트 만들기.
  * **Agentic RAG로 지능형 정보 검색 시스템**: Agentic RAG를 이용하여 더 스마트한 정보 검색 시스템 구축.

---

## 08. Crew AI를 활용한 협업형 에이전트

* 내용: 
  * **Crew AI**를 활용하여 다수의 에이전트가 협업하는 시스템을 만들기
  * 여러 에이전트가 협력하여 **블로그 콘텐츠**를 자동으로 생성하는 시스템 구현해보기

* 주요 내용:
  * **다중 에이전트 블로그 작성기**: 여러 에이전트가 협력하여 블로그 콘텐츠를 작성.
  * **FastAPI, CrewAPI 기반 블로그 콘텐츠 생성기**: FastAPI와 CrewAPI를 이용해 블로그 콘텐츠를 효율적으로 생성.
  * **리액트 통합으로 완성하는 블로그 서비스**: 리액트 프론트엔드와 통합하여 완전한 블로그 시스템 구축.

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