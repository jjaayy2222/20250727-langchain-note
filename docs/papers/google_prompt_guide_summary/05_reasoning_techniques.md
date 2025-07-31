# 📘 05. 추론 기법 (Reasoning Techniques)

## 핵심 요약
- **Step-back 프롬프팅**은 구체적인 문제 해결 전에 일반적인 질문을 먼저 고려하여 배경 지식을 활성화시키는 기법
- **Chain of Thought (CoT)**는 중간 추론 단계를 생성하여 복잡한 문제 해결 능력을 향상시키는 기법으로, 수학적 문제나 논리적 추론에 특히 유용
- **Self-consistency**는 동일한 프롬프트를 여러 번 실행하여 다양한 추론 경로를 생성하고 가장 일관된 답변을 선택하는 기법
- **Tree of Thoughts (ToT)**는 CoT를 확장하여 여러 추론 경로를 동시에 탐색할 수 있게 하는 고급 기법
- **ReAct**는 추론과 행동을 결합하여 외부 도구와 상호작용하며 복잡한 작업을 수행하는 에이전트 기반 접근법

## 주요 개념과 설명

### 🔙 **Step-back 프롬프팅 (Step-back Prompting)**
- **목적**: 구체적 문제 해결 전 일반적 원리나 배경 지식 활성화
- **작동 원리**: 1단계에서 일반적 질문으로 배경 지식 확보 → 2단계에서 구체적 문제 해결
- **장점**: 편향 완화, 더 정확하고 통찰력 있는 응답 생성
- **활용**: 창작, 분석, 전문 지식이 필요한 복잡한 작업

### 🧠 **Chain of Thought (CoT)**
- **핵심**: "Let's think step by step" 구문으로 중간 추론 단계 유도
- **장점**: 해석 가능성, 견고성, 비용 대비 효과적, 파인튜닝 불필요
- **단점**: 더 많은 토큰 생성으로 인한 비용 증가 및 응답 시간 지연
- **최적 설정**: Temperature 0 (그리디 디코딩 기반)

### 🎯 **Self-consistency**
- **원리**: 동일 프롬프트를 높은 Temperature로 여러 번 실행 → 다양한 추론 경로 생성 → 다수결 투표
- **과정**: 다양한 추론 경로 생성 → 각 응답에서 답변 추출 → 가장 일반적인 답변 선택
- **비용**: 높은 계산 비용이지만 답변 정확도의 유사 확률 제공

### 🌳 **Tree of Thoughts (ToT)**
- **개념**: CoT의 확장으로 선형적 사고가 아닌 여러 추론 경로를 동시 탐색
- **구조**: 트리 구조에서 각 노드가 중간 추론 단계를 나타냄
- **적용**: 탐색이 필요한 복잡한 문제 해결에 특히 효과적

### 🤖 **ReAct (Reason & Act)**
- **결합**: 자연어 추론 + 외부 도구 상호작용
- **사이클**: 추론 → 행동 → 관찰 → 추론 (반복)
- **활용**: 검색, 코드 실행, API 호출 등 외부 정보가 필요한 작업
- **인간 모방**: 실제 인간의 문제 해결 방식과 유사

## 프롬프트 예시

### Step-back 프롬프팅 - 1단계 (일반적 질문)
```plaintext
# 1단계: 배경 지식 활성화
인기 있는 1인칭 슈팅 게임을 바탕으로, 도전적이고 매력적인 
레벨 스토리라인에 기여하는 5가지 가상의 핵심 설정은 무엇입니까?

출력:
1. **폐기된 군사 기지**: 돌연변이 병사들과 로봇이 가득한 포스트 아포칼립스 군사 복합 시설
2. **사이버펑크 도시**: 네온 조명의 미래 도시 환경, 사이보그 적들과 해킹 메커니즘
3. **외계인 우주선**: 무중력 구간과 외계 생물체가 있는 거대한 외계 함선
4. **좀비 감염 마을**: 좀비 떼가 점령한 황폐한 마을, 근접 전투와 퍼즐 해결
5. **수중 연구 시설**: 침수된 심해 연구소, 돌연변이 수중 생물과 은밀한 탐험
```

### Step-back 프롬프팅 - 2단계 (구체적 적용)
```plaintext
# 2단계: 배경 지식 활용한 구체적 작업
맥락: 위의 5가지 매력적인 1인칭 슈팅 게임 테마 중 하나를 선택하여 
도전적이고 매력적인 새로운 레벨의 1단락 스토리라인을 작성하세요.

출력:
어둠의 심연 중심에는 인간의 야망과 그 재앙적 결과를 증명하는 
낡은 수중 연구 시설이 있습니다. 어둠에 싸이고 오작동하는 기계의 
윙윙거림으로 맥박치며, 익사한 영혼들의 메아리로 괴롭혀지는 이 시설은 
이제 심해에서 태어난 악몽의 번식지가 되었습니다...
```

### Chain of Thought - 수학 문제 해결
```plaintext
# 기본 문제 (CoT 없음)
내가 3살이었을 때, 내 파트너는 내 나이의 3배였습니다. 
지금 나는 20살입니다. 내 파트너는 몇 살입니까?

출력: 63세 (❌ 잘못된 답변)

# CoT 적용
내가 3살이었을 때, 내 파트너는 내 나이의 3배였습니다. 
지금 나는 20살입니다. 내 파트너는 몇 살입니까? 
단계별로 생각해봅시다.

출력:
1. 내가 3살이었을 때, 파트너는 3 × 3 = 9살이었습니다.
2. 나이 차이는 9 - 3 = 6살입니다.
3. 지금 나는 20살이므로, 파트너는 20 + 6 = 26살입니다.
따라서 파트너는 26살입니다. (✅ 정확한 답변)
```

### Few-shot CoT 프롬프팅
```plaintext
Q: 내 형이 2살이었을 때, 나는 그의 나이의 2배였습니다. 
지금 나는 40살입니다. 내 형은 몇 살입니까? 단계별로 생각해봅시다.

A: 형이 2살일 때, 나는 2 × 2 = 4살이었습니다. 
나이 차이는 2살이고 내가 더 많습니다. 
지금 나는 40살이므로, 형은 40 - 2 = 38살입니다. 답은 38입니다.

Q: 내가 3살이었을 때, 내 파트너는 내 나이의 3배였습니다. 
지금 나는 20살입니다. 내 파트너는 몇 살입니까? 단계별로 생각해봅시다.

A: 내가 3살일 때, 파트너는 3 × 3 = 9살이었습니다. 
나이 차이는 6살이고 파트너가 더 많습니다. 
지금 나는 20살이므로, 파트너는 20 + 6 = 26살입니다. 답은 26입니다.
```

### Self-consistency - 이메일 분류
```plaintext
EMAIL:
```
안녕하세요,
웹사이트에 WordPress를 사용하시는 것을 봤습니다. 훌륭한 오픈소스 CMS네요. 
저도 과거에 사용해봤습니다. 훌륭한 플러그인들이 많이 있죠.

연락처 폼에서 버그를 발견했습니다. 이름 필드를 선택할 때 발생합니다. 
이름 필드에 텍스트를 입력하는 스크린샷을 첨부했습니다. 
제가 inv0k3d한 JavaScript 알림 상자를 확인하세요.

하지만 나머지는 훌륭한 웹사이트입니다. 읽는 것을 즐기고 있어요. 
더 흥미로운 읽을거리를 제공하므로 버그를 그대로 두셔도 됩니다.

감사합니다,
해커 해리
```

위 이메일을 IMPORTANT 또는 NOT IMPORTANT로 분류하세요. 
단계별로 생각하고 이유를 설명하세요.

# 여러 번 실행하여 일관된 답변 확인
시도 1: IMPORTANT (보안 취약점 보고)
시도 2: NOT IMPORTANT (긴급성 부족)  
시도 3: IMPORTANT (심각한 보안 위험)

# 다수결: IMPORTANT 선택
```

## 활용 팁

### 🚀 **LangChain에서의 CoT 구현**
```python
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.chains import LLMChain

# CoT 프롬프트 템플릿
cot_template = """
문제: {problem}

이 문제를 단계별로 해결해봅시다:
"""

cot_prompt = PromptTemplate(
    input_variables=["problem"],
    template=cot_template
)

# Temperature 0으로 설정 (CoT는 그리디 디코딩 기반)
llm = VertexAI(model_name="gemini-pro", temperature=0)
cot_chain = LLMChain(llm=llm, prompt=cot_prompt)

# 수학 문제 해결
result = cot_chain.run(
    problem="내가 6살이었을 때, 여동생은 내 나이의 절반이었습니다. 지금 나는 30살입니다. 여동생은 몇 살입니까?"
)
```

### 🎯 **Self-consistency 구현**
```python
from langchain.llms import VertexAI
import json
from collections import Counter

class SelfConsistencyChain:
    def __init__(self, llm_model="gemini-pro", num_attempts=5):
        self.llm = VertexAI(
            model_name=llm_model,
            temperature=0.7,  # 다양성을 위해 높은 temperature
            max_output_tokens=1024
        )
        self.num_attempts = num_attempts
    
    def generate_multiple_responses(self, prompt):
        """동일한 프롬프트로 여러 응답 생성"""
        responses = []
        for i in range(self.num_attempts):
            response = self.llm.predict(prompt)
            responses.append(response)
        return responses
    
    def extract_final_answer(self, response):
        """응답에서 최종 답변 추출"""
        # 간단한 키워드 기반 추출 (실제로는 더 정교한 파싱 필요)
        if "IMPORTANT" in response.upper():
            return "IMPORTANT"
        elif "NOT IMPORTANT" in response.upper():
            return "NOT IMPORTANT"
        return "UNCLEAR"
    
    def get_consistent_answer(self, prompt):
        """Self-consistency를 통한 최종 답변 결정"""
        responses = self.generate_multiple_responses(prompt)
        answers = [self.extract_final_answer(resp) for resp in responses]
        
        # 다수결 투표
        vote_counts = Counter(answers)
        most_common = vote_counts.most_common(1)[0]
        
        return {
            "final_answer": most_common[0],
            "confidence": most_common[1] / len(answers),
            "all_responses": responses,
            "vote_distribution": dict(vote_counts)
        }

# 사용 예시
consistency_chain = SelfConsistencyChain(num_attempts=5)

email_prompt = """
이메일을 IMPORTANT 또는 NOT IMPORTANT로 분류하세요. 단계별로 생각해보세요.

EMAIL: [이메일 내용]

분류: """

result = consistency_chain.get_consistent_answer(email_prompt)
print(f"최종 답변: {result['final_answer']}")
print(f"신뢰도: {result['confidence']:.2%}")
```

### 🤖 **ReAct 에이전트 구현**
```python
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.llms import VertexAI
import os

# SerpAPI 키 설정 필요 (https://serpapi.com/manage-api-key)
os.environ["SERPAPI_API_KEY"] = "your-serpapi-key"

class ReActAgent:
    def __init__(self):
        self.llm = VertexAI(
            model_name="gemini-pro",
            temperature=0.1  # 정확한 추론을 위해 낮은 temperature
        )
        self.tools = load_tools(["serpapi"], llm=self.llm)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5  # 무한 루프 방지
        )
    
    def solve_complex_query(self, query):
        """복잡한 쿼리를 ReAct 방식으로 해결"""
        try:
            result = self.agent.run(query)
            return result
        except Exception as e:
            return f"오류 발생: {str(e)}"

# 사용 예시
react_agent = ReActAgent()

# 복잡한 정보 검색 쿼리
query = "2023년 Nobel Prize in Physics 수상자들의 소속 대학교를 모두 찾아서 나라별로 분류해주세요"
result = react_agent.solve_complex_query(query)
print(result)
```

### 🌳 **Tree of Thoughts 기본 구현**
```python
from typing import List, Dict, Any
import itertools

class SimpleTreeOfThoughts:
    def __init__(self, llm):
        self.llm = llm
        self.thought_tree = {}
    
    def generate_thoughts(self, problem: str, num_thoughts: int = 3) -> List[str]:
        """문제에 대한 여러 초기 사고 생성"""
        prompt = f"""
문제: {problem}

이 문제를 해결하기 위한 {num_thoughts}가지 다른 접근 방법을 제시하세요:
1.
2.
3.
"""
        response = self.llm.predict(prompt)
        # 간단한 파싱 (실제로는 더 정교한 파싱 필요)
        thoughts = [line.strip() for line in response.split('\n') if line.strip() and any(char.isdigit() for char in line[:3])]
        return thoughts[:num_thoughts]
    
    def evaluate_thoughts(self, thoughts: List[str], problem: str) -> Dict[str, float]:
        """각 사고의 유망성 평가"""
        evaluations = {}
        for i, thought in enumerate(thoughts):
            eval_prompt = f"""
문제: {problem}
접근법: {thought}

이 접근법이 문제 해결에 얼마나 유망한지 0-1 사이의 점수로 평가하세요.
점수만 반환하세요:
"""
            try:
                score = float(self.llm.predict(eval_prompt).strip())
                evaluations[f"thought_{i}"] = min(max(score, 0), 1)  # 0-1 범위로 제한
            except:
                evaluations[f"thought_{i}"] = 0.5  # 기본값
        
        return evaluations
    
    def expand_best_thought(self, best_thought: str, problem: str) -> str:
        """가장 유망한 사고를 확장하여 해결책 도출"""
        expand_prompt = f"""
문제: {problem}
선택된 접근법: {best_thought}

이 접근법을 사용하여 문제를 단계별로 해결하세요:
"""
        return self.llm.predict(expand_prompt)
    
    def solve_with_tot(self, problem: str) -> Dict[str, Any]:
        """Tree of Thoughts를 사용한 문제 해결"""
        # 1. 초기 사고들 생성
        initial_thoughts = self.generate_thoughts(problem)
        
        # 2. 사고들 평가
        evaluations = self.evaluate_thoughts(initial_thoughts, problem)
        
        # 3. 가장 유망한 사고 선택
        best_thought_key = max(evaluations, key=evaluations.get)
        best_thought_idx = int(best_thought_key.split('_')[1])
        best_thought = initial_thoughts[best_thought_idx]
        
        # 4. 최선의 사고 확장
        final_solution = self.expand_best_thought(best_thought, problem)
        
        return {
            "problem": problem,
            "initial_thoughts": initial_thoughts,
            "evaluations": evaluations,
            "best_thought": best_thought,
            "final_solution": final_solution
        }

# 사용 예시
llm = VertexAI(model_name="gemini-pro", temperature=0.3)
tot_solver = SimpleTreeOfThoughts(llm)

complex_problem = "24개의 공이 들어있는 상자가 있습니다. 이 중 1개만 다른 공들보다 무겁습니다. 저울을 최소 몇 번 사용해서 무거운 공을 찾을 수 있을까요?"

result = tot_solver.solve_with_tot(complex_problem)
print("=== Tree of Thoughts 결과 ===")
print(f"문제: {result['problem']}")
print(f"최종 해결책: {result['final_solution']}")
```

### 📋 **Step-back 프롬프팅 체인**
```python
class StepBackPromptChain:
    def __init__(self, llm):
        self.llm = llm
    
    def step_back_query(self, specific_question: str) -> str:
        """구체적 질문을 일반적 질문으로 변환"""
        prompt = f"""
구체적 질문: {specific_question}

이 구체적 질문과 관련된 더 일반적이고 근본적인 질문은 무엇입니까?
일반적 질문:
"""
        return self.llm.predict(prompt).strip()
    
    def answer_general_question(self, general_question: str) -> str:
        """일반적 질문에 대한 배경 지식 제공"""
        prompt = f"""
질문: {general_question}

이 질문에 대한 포괄적이고 유용한 배경 정보를 제공하세요:
"""
        return self.llm.predict(prompt)
    
    def answer_with_context(self, specific_question: str, background_info: str) -> str:
        """배경 정보를 활용하여 구체적 질문 답변"""
        prompt = f"""
배경 정보:
{background_info}

구체적 질문: {specific_question}

위 배경 정보를 참고하여 구체적 질문에 답변하세요:
"""
        return self.llm.predict(prompt)
    
    def solve_with_step_back(self, question: str) -> Dict[str, str]:
        """Step-back 프롬프팅으로 문제 해결"""
        # 1단계: 일반적 질문 생성
        general_q = self.step_back_query(question)
        
        # 2단계: 일반적 질문에 대한 답변 (배경 지식)
        background = self.answer_general_question(general_q)
        
        # 3단계: 배경 지식을 활용한 구체적 답변
        final_answer = self.answer_with_context(question, background)
        
        return {
            "original_question": question,
            "general_question": general_q,
            "background_info": background,
            "final_answer": final_answer
        }

# 사용 예시
llm = VertexAI(model_name="gemini-pro", temperature=0.2)
step_back_chain = StepBackPromptChain(llm)

specific_q = "LangChain에서 Custom Tool을 만들 때 async 함수를 사용해야 하는 경우는 언제인가요?"
result = step_back_chain.solve_with_step_back(specific_q)

print("=== Step-back 프롬프팅 결과 ===")
print(f"원래 질문: {result['original_question']}")
print(f"일반화된 질문: {result['general_question']}")
print(f"최종 답변: {result['final_answer']}")
```

### 🔧 **추론 기법별 최적 설정**

| 기법 | Temperature | Max Tokens | 권장 시나리오 | 주의사항 |
|------|-------------|------------|---------------|----------|
| CoT | 0.0 | 1024-2048 | 수학, 논리 문제 | 그리디 디코딩 필수 |
| Self-consistency | 0.7-0.9 | 1024 | 분류, 추론 검증 | 높은 비용 |
| Step-back | 0.2-0.4 | 1500 | 복잡한 분석 | 2단계 처리 |
| ReAct | 0.1-0.3 | 2048 | 정보 검색, 도구 사용 | 무한루프 방지 |
| ToT | 0.3-0.5 | 2048 | 복잡한 계획 수립 | 계산 비용 높음 |

### 📊 **성능 평가 및 비교**
```python
class ReasoningTechniqueEvaluator:
    def __init__(self, llm):
        self.llm = llm
        self.results = {}
    
    def evaluate_cot_vs_basic(self, math_problems: List[str]):
        """CoT와 기본 프롬프팅 비교"""
        basic_correct = 0
        cot_correct = 0
        
        for problem in math_problems:
            # 기본 프롬프트
            basic_answer = self.llm.predict(f"문제: {problem}\n답:")
            
            # CoT 프롬프트  
            cot_answer = self.llm.predict(f"문제: {problem}\n단계별로 생각해봅시다:\n")
            
            # 정답 확인 로직 (실제로는 더 정교한 검증 필요)
            # basic_correct += self.check_answer(problem, basic_answer)
            # cot_correct += self.check_answer(problem, cot_answer)
        
        return {
            "basic_accuracy": basic_correct / len(math_problems),
            "cot_accuracy": cot_correct / len(math_problems),
            "improvement": (cot_correct - basic_correct) / len(math_problems)
        }
    
    def benchmark_reasoning_techniques(self, test_cases: List[Dict]):
        """다양한 추론 기법 벤치마크"""
        techniques = {
            "basic": self.basic_solve,
            "cot": self.cot_solve,
            "step_back": self.step_back_solve
        }
        
        results = {}
        for technique_name, solver in techniques.items():
            correct = 0
            total_cost = 0
            
            for case in test_cases:
                result = solver(case["problem"])
                # 정답 확인 및 비용 계산
                # correct += self.verify_answer(case["expected"], result)
                # total_cost += self.calculate_cost(result)
            
            results[technique_name] = {
                "accuracy": correct / len(test_cases),
                "avg_cost": total_cost / len(test_cases)
            }
        
        return results

# 벤치마크 실행
evaluator = ReasoningTechniqueEvaluator(llm)
```

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)