# 🛠 LangGraph REACT Agent 트러블슈팅 가이드

> **작성일:** 2025-11-14  
> **작성자:** Jay  
> **소요 시간:** 3시간  

<br>

---

## 1. 초기 시도 (KeyError: Missing variables)

```python
    def run_agent(user_input: str):
        result = agent.invoke({
            "input": user_input,
            "agent_scratchpad": []
        })
        return result["messages"][-1]["content"]

    response = run_agent("How many letters in the word `teddynote`?")
```

**오류 메시지:**

```bash
    KeyError: "Input to ChatPromptTemplate is missing variables {'input', 'agent_scratchpad'}..."
```

**원인:**

* wikidocs 등 예제는 LangChain/LangGraph 이전 버전 기준
* 현 환경의 `create_react_agent`는 **v2 기준**
* 프롬프트 변수가 `{input}` / `{agent_scratchpad}`가 아니라 `messages`, `remaining_steps`를 받음

**해결:**

* 입력 `dict`를 `messages`와 `remaining_steps` 기준으로 변경

```python
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}],
            "remaining_steps": 1
    }) 
```

---

## 2. AIMessage 관련 오류 (TypeError: 'AIMessage' object is not subscriptable)

```python
    return result["messages"][-1]["content"]
```

**오류 메시지:**

```bash
    TypeError: 'AIMessage' object is not subscriptable
```

**원인:**

* 현 환경 v2에서는 `invoke()`가 **AIMessage 객체를 직접 반환**
* dict 형태가 아님 → `result["messages"]` 불가

**해결:**

```python
    # AIMessage 객체의 content 속성 직접 사용
    return result.content
```

> 단, 현 환경에서는 결과가 `dict`일 수도 있으므로 안전하게 처리 필요

---

## 3. ImportError / ModuleNotFoundError

```python
    from langgraph.prebuilt import create_react_agent
    from langchain_core.schema import AIMessage
```

**오류 메시지:**

```bash
    ImportError: cannot import name 'initialize_agent'
ModuleNotFoundError: No module named 'langchain.schema'
```

**원인:**

* LangChain 최신 버전에서 **`initialize_agent` 제거**, `AIMessage` 모듈 경로 변경
* 예제 코드가 오래된 LangChain 기준

**해결:**

```python
    # 현 환경 기준
    from langgraph.prebuilt import create_react_agent
    # AIMessage 필요 시 langchain_core.schema.AIMessage 사용
```

---

## 4. `create_react_agent` 오류 (`TypeError`: `unexpected keyword arguments`)

```python
    agent = create_react_agent(
        model=gpt_5_nano,
        tools=tools,
        verbose=True  # ❌ 현 환경에 없음
    )
```

**오류 메시지:**

```bash
    TypeError: create_react_agent() got unexpected keyword arguments: {'verbose': True}
```

**원인:**

* 현 환경 `create_react_agent`에서는 **verbose 파라미터 제거**
* wikidocs 예제 그대로 복붙하면 무조건 TypeError 발생

**해결:**

```python
    agent = create_react_agent(
        model=gpt_5_nano,
        tools=tools  # tools 없으면 빈 리스트 []
    )
```

---

## 5. 최종 현재 환경용 안전 실행 템플릿

```python
    from langgraph.prebuilt import create_react_agent
    from config import gpt_5_nano 

    # ----------------------------
    # 1. 사용할 도구 정의 (없으면 [])
    tools = []

    # ----------------------------
    # 2. Agent 생성
    agent = create_react_agent(
        model=gpt_5_nano,
        tools=tools
    )

    # ----------------------------
    # 3. 실행 함수
    def run_agent(user_input: str):
        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}],
            "remaining_steps": 1
        })
    
        # 반환값 처리
        if isinstance(result, dict) and "output" in result:
            return result["output"]
        return str(result)

    # ----------------------------
    # 4. 테스트
    response = run_agent("How many letters in the word `teddynote`?")
    print(response)
```

- ✅ 현 환경 v2 기준 안전하게 실행 가능
- ✅ `verbose`, `initialize_agent`, `AIMessage import` 등 **오래된 예제 제거**
- ✅ `dict` / `AIMessage` 반환 안전 처리

---

## 6. 핵심 요약

| 단계 | 문제 원인                   | 해결 방법                                           |
| -- | ----------------------- | ----------------------------------------------- |
| 1  | KeyError, 변수 없음         | `messages`, `remaining_steps`로 입력 변경            |
| 2  | TypeError: AIMessage 불가 | 반환값 객체 확인 후 `.content` 또는 dict `"output"` 사용    |
| 3  | ImportError             | 현 환경 v2 기준 모듈 경로 확인 (`create_react_agent` 사용) |
| 4  | TypeError: verbose      | 현 환경에서 verbose 제거                             |
| 5  | 전체 실패                   | 최신 환경용 템플릿 사용                               |

---