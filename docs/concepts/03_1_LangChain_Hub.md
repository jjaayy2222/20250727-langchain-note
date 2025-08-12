
# 📚 LangChain Hub 프롬프트 주소 & 사용법

## 🚀 LangChain Hub에 프롬프트 등록하기

* `LangSmith` 접속
  * `LangSmith` 접속
  * 로그인 (`Personal 계정` 사용 가능)

* 새 프롬프트 생성
  * 좌측 메뉴에서 `Prompts` 클릭
  * 우측 상단 **`+ Prompt`** 버튼 클릭
  * 원하는 유형 선택
    * `Chat-style prompt` → `대화형` 프롬프트
    * `Instruct-style prompt` → `지시문형` 프롬프트

## 프롬프트 작성

* 예시 (`Chat-style`):

  * `SYSTEM`
  
    ```python
    You are an assistant for question-answering tasks.
    Use the provided context to answer concisely in Korean.
    If you don’t know, say "잘 모르겠습니다."
    ```

  * `HUMAN`

    ```python
    질문: {question}
    문맥: {context}
    답변:
    ```

## 저장 및 이름 설정
  * 화면 상단 `Save` 클릭
  * 저장소 이름 입력 (예: jay-test-prompt)
  * `Private/Public` 선택
	* `Private` → 나만 사용 가능
	* `Public` → 전체 공개


## 저장소 확인
* 저장 후 `좌측 메뉴 Prompts`에서 해당 저장소 클릭
* `Commit` 목록과 `SYSTEM`/`HUMAN` 메시지 확인 가능

## 주소 구조

### 최신 버전
* `username/repo-name`
  * 예: `jay/jay-test-prompt`
  * `URL`: `https://smith.langchain.com/hub/jay/jay-test-prompt`
  
* `특정 커밋 버전` : `username/repo-name:commit-id`
  * 예: `jay/jay-test-prompt:ea749f49`
  * `URL`:`https://smith.langchain.com/hub/jay/jay-test-prompt/ea749f49`



## `LangChain` 코드에서 사용

```python
from langchain import hub

# 최신 버전 가져오기
prompt = hub.pull("jay/jay-test-prompt")

# 특정 커밋 버전 가져오기
prompt = hub.pull("jay/jay-test-prompt:ea749f49")
```

---

## 정리!
  * `hub.pull("username/repo-name")` → 항상 최신 버전 사용
  * `hub.pull("username/repo-name:commit-id")` → 특정 시점 버전 고정
  * 웹에서 직접 확인 가능: `https://smith.langchain.com/hub/username/repo-name`

---
