# **`ConversationKGMemory`의 업데이트된 방법**

## 📚 방법 1: ConversationKGMemory 수동 관리 원리

```python
# ===== 방법 2: ConversationKGMemory를 이용한 수동 메모리 관리 =====
from langchain.memory import ConversationKGMemory
from langchain_openai import ChatOpenAI

# LLM과 메모리 초기화
llm = ChatOpenAI(temperature=0)         # OpenAI GPT 모델 초기화 (일관된 답변을 위해 temperature=0)
memory = ConversationKGMemory(llm=llm)  # 지식 그래프 메모리 생성 (LLM을 이용해 엔티티와 관계를 추출)

# 🔍 ConversationKGMemory의 핵심 원리:
# 1. 대화 내용을 분석하여 '주어-관계-목적어' 형태의 지식 트리플(Knowledge Triplet)을 자동 생성
# 2. 예: "Teddy works with Shirley", "Shirley is a designer" 같은 관계를 추출
# 3. 이런 지식들을 그래프 형태로 저장하여 나중에 활용

# 첫 번째 대화 저장 - save_context()로 입력과 출력을 메모리에 저장
memory.save_context(
    # 사용자 입력: Teddy라는 이름과 Shirley가 동료이자 새 디자이너라는 정보 포함
    {"input": "My name is Teddy. Shirley is a coworker of mine, and she's a new designer at our company."},
    # AI 출력: 대화 맥락을 이어가는 응답
    {"output": "Nice to meet you, Teddy! It's great to hear that Shirley is joining as a new designer. How are you finding working with her so far?"}
)

# 🧠 이 시점에서 ConversationKGMemory는 내부적으로:
# - "Teddy" (엔티티), "Shirley" (엔티티), "coworker" (관계), "designer" (속성) 등을 추출
# - 지식 그래프 형태로 정보를 구조화하여 저장

# 메모리 내용 확인 - 특정 질문에 대해 관련 정보 추출
history = memory.load_memory_variables({"input": "Who is Shirley?"})  

# 🔍 이 메서드는 "Shirley"와 관련된 모든 지식 트리플을 찾아서 반환
print(history)  # {'history': 'On Shirley: Shirley is a coworker. Shirley is a designer.'} 형태로 출력

# 지식 트리플 직접 확인 - 특정 문장에서 추출된 지식 관계들 보기
triplets = memory.get_knowledge_triplets("Shirley is a designer")

# 🔍 입력된 문장을 분석하여 주어-동사-목적어 관계를 추출
print(triplets)  # [('Shirley', 'is', 'designer')] 같은 형태로 출력
```

<br>

## 🚀 방법 2: LangGraph 최신 방식 원리

```python
# ===== 방법 3: LangGraph를 사용한 최신 대화 구조 및 메모리 관리 =====
import uuid
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_openai import ChatOpenAI

# 🎯 LangGraph의 핵심 개념:
# 1. 상태 기반 워크플로우: 대화를 상태(State)의 변화로 관리
# 2. 그래프 구조: 노드(처리 단위)와 엣지(연결)로 대화 흐름 제어
# 3. 체크포인트: 각 단계의 상태를 저장하여 세션 지속성 보장

def create_conversation_graph():
    """대화 처리를 위한 그래프 기반 워크플로우 생성 함수"""
    llm = ChatOpenAI(temperature=0)  # LLM 모델 초기화
    
    def call_model(state: MessagesState):
        """
        그래프의 핵심 처리 노드 - 실제 LLM 호출 담당
        :param state: 현재 대화 상태 (이전 메시지들 포함)
        :return: LLM 응답이 추가된 새로운 상태
        """
        # 🔄 상태에 저장된 모든 메시지를 LLM에 전달
        response = llm.invoke(state["messages"])
        # 📝 LLM 응답을 상태에 추가하여 반환
        return {"messages": response}
    
    # 📊 StateGraph: 대화 상태를 관리하는 그래프 구조 생성
    workflow = StateGraph(state_schema=MessagesState)  # MessagesState: 메시지 리스트를 포함하는 상태 스키마
    
    # 🔗 그래프 구조 정의
    workflow.add_edge(START, "model")  # 시작점에서 "model" 노드로 연결
    workflow.add_node("model", call_model)  # "model" 노드에 call_model 함수 연결
    
    # 💾 MemorySaver: 대화 세션의 지속성을 위한 체크포인트 메커니즘
    memory = MemorySaver()  # 메모리 상태를 자동으로 저장/복원
    
    # 🔧 그래프 컴파일: 실행 가능한 워크플로우로 변환
    app = workflow.compile(checkpointer=memory)  # checkpointer로 메모리 연결
    
    return app

# 🎬 대화 실행 예시
app = create_conversation_graph()  # 대화 그래프 생성

# 🆔 세션 관리를 위한 고유 식별자 생성
thread_id = str(uuid.uuid4())  # 각 대화 세션마다 고유한 ID
config = {"configurable": {"thread_id": thread_id}}  # 설정에 세션 ID 포함

# 💬 사용자 메시지 생성
input_message = HumanMessage(
    content="My name is Teddy. Shirley is a coworker of mine, and she's a new designer at our company."
)

# 🔄 대화 스트리밍 실행
for event in app.stream(
    {"messages": [input_message]},  # 초기 메시지 상태
    config,  # 세션 설정
    stream_mode="values"  # 각 단계의 전체 상태 반환
):
    # 📤 최신 메시지 (LLM 응답) 출력
    event["messages"][-1].pretty_print()  # 마지막 메시지만 예쁘게 출력
```

## 🔄 두 방법의 핵심 차이점

### **방법 1 (`ConversationKGMemory`)**
- **지식 추출**: 대화에서 엔티티와 관계를 자동 추출
- **구조화**: 지식을 그래프 형태로 저장
- **질의**: 특정 엔티티에 대한 정보를 빠르게 검색 가능
- **한계**: 단순한 체인 구조, 복잡한 워크플로우 처리 어려움

### **방법 2 (`LangGraph`)**
- **상태 관리**: 대화 전체를 상태로 관리하여 더 유연
- **워크플로우**: 복잡한 대화 흐름 제어 가능
- **확장성**: 여러 노드와 조건부 분기 지원
- **현대적**: `LangChain`의 최신 아키텍처 반영

