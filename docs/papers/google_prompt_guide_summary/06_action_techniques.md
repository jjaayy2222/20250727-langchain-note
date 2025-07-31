# 📘 06. 행동 기반 기법 (Action-based Techniques)

## 핵심 요약
- **ReAct (Reason & Act)**는 자연어 추론과 외부 도구 상호작용을 결합하여 복잡한 작업을 수행하는 에이전트 기반 접근법
- **사고-행동-관찰 루프**를 통해 인간의 실제 문제 해결 방식을 모방하며, 외부 정보 검색이 필요한 작업에 특히 효과적
- **Automatic Prompt Engineering (APE)**는 프롬프트 작성을 자동화하여 인간의 개입 없이도 모델 성능을 향상시키는 기법
- **반복적 개선**을 통해 후보 프롬프트들을 생성하고 평가하여 최적의 프롬프트를 선택하는 과정

## 주요 개념과 설명

### 🤖 **ReAct (Reason & Act)**
- **핵심 개념**: 추론(Reasoning) + 행동(Acting)을 반복적으로 수행
- **작동 원리**: 
  1. **추론**: 문제 분석 및 다음 행동 계획
  2. **행동**: 외부 도구 사용 (검색, API 호출, 코드 실행 등)
  3. **관찰**: 행동 결과 확인
  4. **반복**: 목표 달성까지 사이클 지속
- **장점**: 외부 정보 접근, 동적 문제 해결, 해석 가능성 제공

### 🛠️ **ReAct의 구성 요소**
- **Tools**: 검색 엔진, 계산기, 데이터베이스, API 등
- **Agent**: 추론과 도구 선택을 담당하는 LLM
- **Memory**: 이전 상호작용 기록 저장
- **Controller**: 전체 프로세스 관리 및 종료 조건 제어

### 🔄 **Automatic Prompt Engineering (APE)**
- **목적**: 프롬프트 작성 과정 자동화
- **방법론**:
  1. 초기 프롬프트 후보들 생성
  2. 각 후보의 성능 평가
  3. 최고 성능 후보 선택
  4. 선택된 프롬프트 개선 및 반복
- **평가 지표**: BLEU, ROUGE, 정확도, F1-score 등

## 프롬프트 예시

### ReAct 패턴 - 정보 검색 작업
```plaintext
# 문제
Metallica 밴드 멤버들의 자녀 수를 모두 합하면 몇 명인가요?

# ReAct 추론 과정
생각: Metallica는 4명의 멤버로 구성된 밴드입니다. 각 멤버의 자녀 수를 알아봐야 합니다.

행동: 검색
행동 입력: James Hetfield 자녀 수

관찰: James Hetfield는 3명의 자녀가 있습니다.

생각: 1/4 Metallica 밴드 멤버가 3명의 자녀를 가지고 있습니다.

행동: 검색  
행동 입력: Lars Ulrich 자녀 수

관찰: Lars Ulrich는 3명의 자녀가 있습니다.

생각: 2/4 Metallica 밴드 멤버가 총 6명의 자녀를 가지고 있습니다.

행동: 검색
행동 입력: Kirk Hammett 자녀 수

관찰: Kirk Hammett는 두 번째 아내 Lani와 1998년부터 결혼했으며, 
Angel(2006년생)과 Vincenzo(2008년생) 두 아들이 있습니다.

생각: 3/4 Metallica 밴드 멤버가 총 8명의 자녀를 가지고 있습니다.

행동: 검색
행동 입력: Robert Trujillo 자녀 수

관찰: Robert Trujillo는 2명의 자녀가 있습니다.

생각: 4/4 Metallica 밴드 멤버가 총 10명의 자녀를 가지고 있습니다.

최종 답변: 10명
```

### APE - 프롬프트 생성 자동화
```plaintext
# 단계 1: 프롬프트 후보 생성
우리는 밴드 굿즈 티셔츠 웹샵을 운영하며, 챗봇 훈련을 위해 
"Metallica 티셔츠 S사이즈 1개 주문"과 같은 의미의 다양한 표현이 필요합니다. 
동일한 의미를 가진 10가지 변형을 생성하세요.

# 생성된 후보들:
1. S사이즈 Metallica 티셔츠 구매하고 싶어요
2. Metallica 티셔츠 스몰 사이즈로 주문할 수 있나요?
3. 작은 사이즈 Metallica 티셔츠 하나 주세요
4. Metallica 셔츠 S 사이즈 한 장 부탁드립니다
5. S 사이즈 Metallica 티셔츠 1개 원합니다
6. 스몰 사이즈 Metallica 티셔츠 주문하겠습니다
7. Metallica 작은 사이즈 티셔츠 하나 찾고 있어요
8. S사이즈 Metallica 티셔츠 하나 구할 수 있나요?
9. 작은 사이즈로 Metallica 티셔츠 한 장 주세요
10. Metallica 스몰 티셔츠 1개 주문하겠습니다

# 단계 2: 평가 및 선택
# 각 후보를 BLEU/ROUGE 스코어로 평가하여 최적 후보 선택
```

## 활용 팁

### 🚀 **LangChain ReAct 에이전트 구현**
```python
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.llms import VertexAI
from langchain.tools import Tool
import os

# 환경 변수 설정
os.environ["SERPAPI_API_KEY"] = "your-serpapi-key"

class ReActAgent:
    def __init__(self, model_name="gemini-pro"):
        self.llm = VertexAI(
            model_name=model_name,
            temperature=0.1,  # 정확한 추론을 위해 낮은 온도
            max_output_tokens=2048
        )
        
        # 기본 도구 로드
        self.tools = load_tools(["serpapi", "llm-math"], llm=self.llm)
        
        # 커스텀 도구 추가
        self.tools.append(self._create_korean_search_tool())
        
        # 에이전트 초기화
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5,  # 무한 루프 방지
            early_stopping_method="generate"
        )
    
    def _create_korean_search_tool(self):
        """한국어 검색에 특화된 커스텀 도구"""
        def korean_search(query: str) -> str:
            # 한국어 검색 로직 구현
            return f"한국어 검색 결과: {query}에 대한 정보..."
        
        return Tool(
            name="Korean Search",
            description="한국어 정보를 검색할 때 사용하는 도구",
            func=korean_search
        )
    
    def solve_complex_query(self, query: str) -> str:
        """복잡한 쿼리를 ReAct 방식으로 해결"""
        try:
            result = self.agent.run(query)
            return result
        except Exception as e:
            return f"에러 발생: {str(e)}"

# 사용 예시
react_agent = ReActAgent()

# 복잡한 정보 검색 및 계산
query = """
2023년 노벨 물리학상 수상자들의 소속 대학교를 찾고, 
각 대학교가 위치한 나라별로 분류해주세요.
"""

result = react_agent.solve_complex_query(query)
print(result)
```

### 🎯 **커스텀 ReAct 체인 구현**
```python
from typing import List, Dict, Any, Optional
import json

class CustomReActChain:
    def __init__(self, llm, tools: List[Tool]):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.memory = []
        self.max_iterations = 10
    
    def _format_tools_description(self) -> str:
        """도구 설명 포맷"""
        descriptions = []
        for tool_name, tool in self.tools.items():
            descriptions.append(f"- {tool_name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _parse_action(self, text: str) -> Optional[Dict[str, str]]:
        """응답에서 행동과 입력 파싱"""
        try:
            lines = text.strip().split('\n')
            action = None
            action_input = None
            
            for line in lines:
                if line.startswith('행동:') or line.startswith('Action:'):
                    action = line.split(':', 1)[1].strip()
                elif line.startswith('행동 입력:') or line.startswith('Action Input:'):
                    action_input = line.split(':', 1)[1].strip()
            
            if action and action_input:
                return {"action": action, "action_input": action_input}
            return None
        except:
            return None
    
    def _execute_tool(self, action: str, action_input: str) -> str:
        """도구 실행"""
        if action in self.tools:
            try:
                result = self.tools[action].run(action_input)
                return str(result)
            except Exception as e:
                return f"도구 실행 오류: {str(e)}"
        else:
            return f"알 수 없는 도구: {action}. 사용 가능한 도구: {list(self.tools.keys())}"
    
    def solve(self, question: str) -> Dict[str, Any]:
        """ReAct 방식으로 문제 해결"""
        
        # 초기 프롬프트
        initial_prompt = f"""
다음 질문에 답하기 위해 단계별로 추론하고 필요시 도구를 사용하세요.

사용 가능한 도구:
{self._format_tools_description()}

도구 사용 형식:
생각: [현재 상황에 대한 분석]
행동: [도구 이름]
행동 입력: [도구에 전달할 입력]
관찰: [도구 실행 결과를 기다림]

질문: {question}

생각:"""

        conversation_history = initial_prompt
        
        for iteration in range(self.max_iterations):
            # LLM에게 응답 요청
            response = self.llm.predict(conversation_history)
            conversation_history += response
            
            # 행동 파싱
            action_dict = self._parse_action(response)
            
            if action_dict:
                # 도구 실행
                observation = self._execute_tool(
                    action_dict["action"], 
                    action_dict["action_input"]
                )
                
                # 대화 기록에 관찰 결과 추가
                conversation_history += f"\n관찰: {observation}\n\n생각:"
                
                # 메모리에 저장
                self.memory.append({
                    "iteration": iteration + 1,
                    "thought": response,
                    "action": action_dict["action"],
                    "action_input": action_dict["action_input"],
                    "observation": observation
                })
            else:
                # 최종 답변으로 간주
                final_answer = response.split("최종 답변:")[-1].strip() if "최종 답변:" in response else response
                
                return {
                    "question": question,
                    "final_answer": final_answer,
                    "reasoning_steps": self.memory,
                    "total_iterations": iteration + 1,
                    "full_conversation": conversation_history
                }
        
        return {
            "question": question,
            "final_answer": "최대 반복 횟수에 도달했습니다.",
            "reasoning_steps": self.memory,
            "total_iterations": self.max_iterations,
            "full_conversation": conversation_history
        }

# 사용 예시
from langchain.tools import DuckDuckGoSearchRun, Calculator

# 도구 정의
search = DuckDuckGoSearchRun()
calculator = Calculator()

tools = [
    Tool(name="Search", description="인터넷 검색", func=search.run),
    Tool(name="Calculator", description="수학 계산", func=calculator.run)
]

# 커스텀 ReAct 체인 실행
llm = VertexAI(model_name="gemini-pro", temperature=0.1)
react_chain = CustomReActChain(llm, tools)

result = react_chain.solve("BTS 멤버 수와 BLACKPINK 멤버 수를 더한 값은?")
print(f"최종 답변: {result['final_answer']}")
```

### 🔄 **Automatic Prompt Engineering 구현**
```python
from typing import List, Tuple
import numpy as np
from sklearn.metrics import accuracy_score
import itertools

class AutomaticPromptEngineer:
    def __init__(self, llm, evaluation_llm=None):
        self.llm = llm
        self.evaluation_llm = evaluation_llm or llm
        self.prompt_candidates = []
        self.evaluation_results = []
    
    def generate_prompt_candidates(self, task_description: str, num_candidates: int = 10) -> List[str]:
        """프롬프트 후보들 생성"""
        generation_prompt = f"""
작업 설명: {task_description}

이 작업을 수행하기 위한 {num_candidates}가지 다른 프롬프트를 생성하세요. 
각각 다른 접근 방식과 스타일을 사용하세요.

프롬프트 1:
프롬프트 2:
...
"""
        
        response = self.llm.predict(generation_prompt)
        
        # 응답에서 프롬프트들 추출 (간단한 파싱)
        candidates = []
        lines = response.split('\n')
        current_prompt = ""
        
        for line in lines:
            if line.startswith('프롬프트 ') and current_prompt:
                candidates.append(current_prompt.strip())
                current_prompt = ""
            elif line.startswith('프롬프트 '):
                current_prompt = line.split(':', 1)[1].strip() if ':' in line else ""
            else:
                current_prompt += " " + line.strip()
        
        if current_prompt:
            candidates.append(current_prompt.strip())
        
        self.prompt_candidates = candidates[:num_candidates]
        return self.prompt_candidates
    
    def evaluate_prompts(self, test_cases: List[Dict[str, str]], metric: str = "accuracy") -> List[float]:
        """프롬프트 후보들 평가"""
        scores = []
        
        for prompt in self.prompt_candidates:
            if metric == "accuracy":
                score = self._evaluate_accuracy(prompt, test_cases)
            elif metric == "bleu":
                score = self._evaluate_bleu(prompt, test_cases)
            else:
                score = self._evaluate_custom(prompt, test_cases, metric)
            
            scores.append(score)
        
        self.evaluation_results = scores
        return scores
    
    def _evaluate_accuracy(self, prompt: str, test_cases: List[Dict[str, str]]) -> float:
        """정확도 기반 평가"""
        correct = 0
        total = len(test_cases)
        
        for case in test_cases:
            full_prompt = prompt + "\n\n" + case["input"]
            try:
                response = self.llm.predict(full_prompt)
                predicted = response.strip().upper()
                expected = case["expected"].strip().upper()
                
                if predicted == expected:
                    correct += 1
            except:
                continue
        
        return correct / total if total > 0 else 0.0
    
    def _evaluate_bleu(self, prompt: str, test_cases: List[Dict[str, str]]) -> float:
        """BLEU 스코어 기반 평가"""
        from nltk.translate.bleu_score import sentence_bleu
        
        total_bleu = 0
        count = 0
        
        for case in test_cases:
            full_prompt = prompt + "\n\n" + case["input"]
            try:
                response = self.llm.predict(full_prompt)
                reference = [case["expected"].split()]
                candidate = response.strip().split()
                
                bleu = sentence_bleu(reference, candidate)
                total_bleu += bleu
                count += 1
            except:
                continue
        
        return total_bleu / count if count > 0 else 0.0
    
    def select_best_prompt(self) -> Tuple[str, float]:
        """최고 성능 프롬프트 선택"""
        if not self.evaluation_results:
            raise ValueError("먼저 프롬프트 평가를 실행하세요.")
        
        best_idx = np.argmax(self.evaluation_results)
        best_prompt = self.prompt_candidates[best_idx]
        best_score = self.evaluation_results[best_idx]
        
        return best_prompt, best_score
    
    def improve_prompt(self, base_prompt: str, improvement_type: str = "optimize") -> List[str]:
        """프롬프트 개선"""
        improvement_prompt = f"""
기본 프롬프트: {base_prompt}

이 프롬프트를 다음 방향으로 개선한 3가지 버전을 만들어주세요:
1. 더 명확하고 구체적으로
2. 더 간결하고 효율적으로  
3. 더 창의적이고 다양한 접근으로

개선된 프롬프트 1:
개선된 프롬프트 2:
개선된 프롬프트 3:
"""
        
        response = self.llm.predict(improvement_prompt)
        # 파싱 로직 구현
        improved_prompts = self._parse_improved_prompts(response)
        
        return improved_prompts
    
    def run_ape_cycle(self, task_description: str, test_cases: List[Dict], iterations: int = 3) -> Dict:
        """전체 APE 사이클 실행"""
        best_prompts = []
        
        for iteration in range(iterations):
            print(f"=== APE 반복 {iteration + 1} ===")
            
            # 1단계: 프롬프트 후보 생성
            if iteration == 0:
                candidates = self.generate_prompt_candidates(task_description)
            else:
                # 이전 최고 프롬프트를 기반으로 개선
                best_prompt, _ = self.select_best_prompt()
                candidates = self.improve_prompt(best_prompt)
                self.prompt_candidates = candidates
            
            # 2단계: 평가
            scores = self.evaluate_prompts(test_cases)
            
            # 3단계: 최고 성능 선택
            best_prompt, best_score = self.select_best_prompt()
            best_prompts.append((best_prompt, best_score))
            
            print(f"반복 {iteration + 1} 최고 점수: {best_score:.3f}")
        
        # 전체 반복에서 최고 성능 프롬프트 선택
        final_best = max(best_prompts, key=lambda x: x[1])
        
        return {
            "best_prompt": final_best[0],
            "best_score": final_best[1],
            "iteration_results": best_prompts,
            "all_candidates": self.prompt_candidates,
            "all_scores": self.evaluation_results
        }

# 사용 예시
llm = VertexAI(model_name="gemini-pro", temperature=0.7)
ape = AutomaticPromptEngineer(llm)

# 테스트 케이스 정의
test_cases = [
    {"input": "이 영화는 정말 훌륭했습니다!", "expected": "POSITIVE"},
    {"input": "시간 낭비였어요.", "expected": "NEGATIVE"},
    {"input": "그냥 그랬어요.", "expected": "NEUTRAL"}
]

# APE 실행
result = ape.run_ape_cycle(
    task_description="영화 리뷰를 POSITIVE, NEGATIVE, NEUTRAL로 분류",
    test_cases=test_cases,
    iterations=3
)

print(f"최종 최적 프롬프트: {result['best_prompt']}")
print(f"성능 점수: {result['best_score']:.3f}")
```

### 📊 **성능 모니터링 및 최적화**
```python
class ReActPerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "avg_iterations": 0,
            "tool_usage": {},
            "error_types": {},
            "response_times": []
        }
    
    def log_query(self, query: str, result: Dict, execution_time: float):
        """쿼리 실행 결과 로깅"""
        self.metrics["total_queries"] += 1
        
        if result.get("final_answer") and "오류" not in result["final_answer"]:
            self.metrics["successful_queries"] += 1
        
        # 평균 반복 횟수 업데이트
        iterations = result.get("total_iterations", 0)
        current_avg = self.metrics["avg_iterations"]
        total = self.metrics["total_queries"]
        self.metrics["avg_iterations"] = (current_avg * (total - 1) + iterations) / total
        
        # 도구 사용 통계
        for step in result.get("reasoning_steps", []):
            tool = step.get("action")
            if tool:
                self.metrics["tool_usage"][tool] = self.metrics["tool_usage"].get(tool, 0) + 1
        
        # 응답 시간 기록
        self.metrics["response_times"].append(execution_time)
    
    def get_performance_report(self) -> Dict:
        """성능 보고서 생성"""
        if self.metrics["total_queries"] == 0:
            return {"message": "실행된 쿼리가 없습니다."}
        
        success_rate = self.metrics["successful_queries"] / self.metrics["total_queries"]
        avg_response_time = np.mean(self.metrics["response_times"])
        
        return {
            "총 쿼리 수": self.metrics["total_queries"],
            "성공률": f"{success_rate:.2%}",
            "평균 반복 횟수": f"{self.metrics['avg_iterations']:.2f}",
            "평균 응답 시간": f"{avg_response_time:.2f}초",
            "도구 사용 빈도": self.metrics["tool_usage"],
            "가장 많이 사용된 도구": max(self.metrics["tool_usage"].items(), key=lambda x: x[1]) if self.metrics["tool_usage"] else None
        }

# 성능 모니터링 통합
class MonitoredReActAgent(ReActAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor = ReActPerformanceMonitor()
    
    def solve_complex_query(self, query: str) -> str:
        import time
        start_time = time.time()
        
        try:
            result = super().solve_complex_query(query)
            execution_time = time.time() - start_time
            
            # 성능 데이터 로깅
            self.monitor.log_query(query, {"final_answer": result}, execution_time)
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = {"final_answer": f"오류: {str(e)}"}
            self.monitor.log_query(query, error_result, execution_time)
            raise
    
    def get_performance_summary(self):
        return self.monitor.get_performance_report()

# 사용법
monitored_agent = MonitoredReActAgent()

# 여러 쿼리 실행
queries = [
    "서울의 현재 날씨는?",
    "파이썬으로 피보나치 수열 구현하는 방법은?",
    "2024년 AI 트렌드는?"
]

for query in queries:
    try:
        result = monitored_agent.solve_complex_query(query)
        print(f"Q: {query}")
        print(f"A: {result}\n")
    except Exception as e:
        print(f"오류 발생: {e}\n")

# 성능 요약 확인
print("=== 성능 요약 ===")
print(monitored_agent.get_performance_summary())
```

### 🎯 **작업별 ReAct 최적화 가이드**

| 작업 유형 | 권장 도구 | Temperature | Max Iterations | 주의사항 |
|-----------|-----------|-------------|----------------|----------|
| 정보 검색 | Search, Calculator | 0.1-0.3 | 5-7 | 검색 쿼리 품질 |
| 데이터 분석 | Python REPL, SQL | 0.2-0.4 | 8-10 | 코드 검증 필요 |
| 창작 지원 | Search, Knowledge | 0.5-0.7 | 3-5 | 창의성과 정확성 균형 |
| 문제 해결 | Calculator, Search | 0.1-0.2 | 7-12 | 논리적 단계 확인 |

### 🔧 **ReAct 디버깅 및 최적화**
```python
class ReActDebugger:
    def __init__(self, agent):
        self.agent = agent
        self.debug_logs = []
    
    def debug_solve(self, query: str, verbose: bool = True) -> Dict:
        """디버깅 모드로 ReAct 실행"""
        result = self.agent.solve_complex_query(query)
        
        debug_info = {
            "query": query,
            "result": result,
            "reasoning_analysis": self._analyze_reasoning(),
            "tool_efficiency": self._analyze_tool_usage(),
            "suggestions": self._generate_suggestions()
        }
        
        if verbose:
            self._print_debug_info(debug_info)
        
        return debug_info
    
    def _analyze_reasoning(self) -> Dict:
        """추론 과정 분석"""
        return {
            "logical_flow": "양호",
            "redundant_steps": 0,
            "missing_steps": []
        }
    
    def _analyze_tool_usage(self) -> Dict:
        """도구 사용 효율성 분석"""
        return {
            "appropriate_tools": True,
            "tool_sequence": "최적",
            "unused_tools": []
        }
    
    def _generate_suggestions(self) -> List[str]:
        """개선 제안 생성"""
        return [
            "검색 쿼리를 더 구체적으로 작성",
            "중간 결과 검증 단계 추가",
            "도구 선택 기준 명확화"
        ]

# 디버거 사용
debugger = ReActDebugger(react_agent)
debug_result = debugger.debug_solve("복잡한 수학 문제를 해결해주세요")
```

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)