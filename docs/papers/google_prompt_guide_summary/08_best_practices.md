# 📘 08. 모범 사례 및 팁 (Best Practices & Tips)

## 핵심 요약
- **예시 제공**은 프롬프트 엔지니어링에서 가장 중요한 모범 사례로, Few-shot 프롬프팅을 통해 모델 성능을 극적으로 향상시킴
- **명확하고 구체적인 지시사항**이 제약사항보다 효과적이며, 모델이 원하는 결과를 정확히 이해할 수 있도록 도움
- **구조화된 출력 형식(JSON, XML)**은 일관성을 보장하고 할루시네이션을 줄이며 후처리 작업을 용이하게 함
- **반복적 실험과 문서화**가 필수이며, 프롬프트 버전 관리와 성능 추적을 통해 지속적인 개선이 가능
- **모델별 최적화**가 중요하며, 모델 업데이트와 새로운 기능에 맞춰 프롬프트를 조정해야 함

## 주요 개념과 설명

### 🎯 **예시 제공의 중요성**
- **학습 효과**: 모델이 원하는 출력 패턴을 이해하고 모방할 수 있게 함
- **정확성 향상**: 구체적인 예시를 통해 모델의 추측을 줄이고 정확한 결과 생성
- **일관성 확보**: 동일한 유형의 작업에서 일관된 품질과 형식 유지

### 📝 **명확한 지시사항 설계**
- **단순성 원칙**: 복잡한 언어나 불필요한 정보 제거
- **행동 지향적 동사**: Analyze, Create, Extract, Generate 등 명확한 동작 지시
- **구체적 출력 요구**: 원하는 결과의 형식, 길이, 스타일 명시

### 🔧 **구조화된 출력 활용**
- **JSON/XML 형식**: 파싱 용이성, 데이터 타입 보장, 관계 인식 향상
- **스키마 정의**: 입력과 출력 모두에 대한 명확한 구조 제공
- **오류 방지**: 구조화를 통한 할루시네이션 감소

## 프롬프트 예시

### 모범 사례 적용 - BEFORE/AFTER

#### ❌ 개선 전 (비효율적)
```plaintext
뉴욕에 지금 가고 있는데, 좋은 장소들에 대해 더 듣고 싶습니다. 
3살짜리 아이 둘과 함께 있어요. 휴가 동안 어디로 가야 할까요?
```

#### ✅ 개선 후 (효율적)
```plaintext
역할: 관광객을 위한 여행 가이드로 활동하세요.

작업: 3세 아이와 함께 뉴욕 맨해튼에서 방문하기 좋은 장소들을 설명해주세요.

출력 형식:
- 장소명: [이름]
- 위치: [주소/지역]
- 아이 친화도: [1-5점]
- 추천 이유: [간단한 설명]
- 소요 시간: [예상 시간]

장소 3곳을 추천해주세요.
```

### 구조화된 출력 - 제품 분석
```plaintext
다음 제품 정보를 분석하고 JSON 형식으로 반환하세요:

입력 스키마:
```
{
  "name": "제품명",
  "category": "카테고리",
  "price": 가격(숫자),
  "features": ["기능1", "기능2"],
  "release_date": "YYYY-MM-DD"
}
```

분석할 제품:
"iPhone 15 Pro는 2023년 9월 출시된 애플의 최신 스마트폰입니다. 
가격은 $999이며, A17 Pro 칩, 48MP 카메라, 티타늄 디자인이 특징입니다."

출력 JSON:
```

**출력**:
```json
{
  "name": "iPhone 15 Pro",
  "category": "스마트폰",
  "price": 999,
  "features": ["A17 Pro 칩", "48MP 카메라", "티타늄 디자인"],
  "release_date": "2023-09-01",
  "analysis": {
    "target_market": "프리미엄 사용자",
    "competitive_advantage": "고성능 칩셋과 프로급 카메라",
    "price_segment": "플래그십"
  }
}
```

## 활용 팁

### 🚀 **LangChain 모범 사례 구현**

#### 프롬프트 템플릿 관리 시스템
```python
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class PromptConfig:
    """프롬프트 설정 관리"""
    name: str
    goal: str
    model: str
    temperature: float
    max_tokens: int
    top_k: int
    top_p: float
    version: str

class BestPracticePromptManager:
    def __init__(self):
        self.templates = {}
        self.examples = {}
        self.configs = {}
    
    def create_few_shot_template(self, name: str, examples: List[Dict], 
                               example_template: str, prefix: str, 
                               suffix: str, input_variables: List[str]):
        """Few-shot 템플릿 생성 (모범 사례: 예시 제공)"""
        
        example_prompt = PromptTemplate(
            input_variables=list(examples[0].keys()),
            template=example_template
        )
        
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=input_variables,
            example_separator="\n---\n"  # 예시 구분을 명확히
        )
        
        self.templates[name] = few_shot_prompt
        self.examples[name] = examples
        
        return few_shot_prompt
    
    def create_structured_output_template(self, name: str, task: str, 
                                        output_schema: Dict, input_vars: List[str]):
        """구조화된 출력 템플릿 생성"""
        
        schema_str = json.dumps(output_schema, indent=2, ensure_ascii=False)
        
        template = f"""
작업: {task}

출력 스키마:
```
{schema_str}
```

입력: {{input_data}}

위 스키마에 맞는 정확한 JSON을 생성하세요. 다른 텍스트는 포함하지 마세요.

JSON 출력:
"""
        
        prompt = PromptTemplate(
            input_variables=input_vars,
            template=template
        )
        
        self.templates[name] = prompt
        return prompt
    
    def create_instruction_based_template(self, name: str, role: str, 
                                        instructions: List[str], 
                                        output_format: str):
        """지시사항 기반 템플릿 (제약보다 지시사항 우선)"""
        
        instructions_str = "\n".join([f"- {inst}" for inst in instructions])
        
        template = f"""
역할: {role}

지시사항:
{instructions_str}

출력 형식: {output_format}

입력: {{input}}

응답:
"""
        
        prompt = PromptTemplate(
            input_variables=["input"],
            template=template
        )
        
        self.templates[name] = prompt
        return prompt

# 사용 예시
manager = BestPracticePromptManager()

# 1. Few-shot 분류 템플릿 생성
classification_examples = [
    {"input": "이 제품 정말 좋아요! 추천합니다.", "output": "POSITIVE"},
    {"input": "그냥 그런 것 같아요.", "output": "NEUTRAL"},
    {"input": "완전 실망이에요. 돈 아까워요.", "output": "NEGATIVE"},
    {"input": "기대했던 것보다 훨씬 좋네요!", "output": "POSITIVE"},
    {"input": "보통 수준이네요. 특별하지 않아요.", "output": "NEUTRAL"}
]

sentiment_template = manager.create_few_shot_template(
    name="sentiment_classification",
    examples=classification_examples,
    example_template="입력: {input}\n분류: {output}",
    prefix="고객 리뷰를 POSITIVE, NEUTRAL, NEGATIVE로 분류하세요.\n\n예시:",
    suffix="\n입력: {review}\n분류:",
    input_variables=["review"]
)

# 2. 구조화된 출력 템플릿
product_schema = {
    "name": "제품명",
    "category": "카테고리",
    "sentiment": "POSITIVE|NEUTRAL|NEGATIVE",
    "key_features": ["기능1", "기능2"],
    "price_mentioned": "boolean",
    "recommendation_score": "1-5 숫자"
}

product_analysis_template = manager.create_structured_output_template(
    name="product_analysis",
    task="제품 리뷰를 분석하여 구조화된 정보 추출",
    output_schema=product_schema,
    input_vars=["input_data"]
)
```

#### 동적 프롬프트 최적화 시스템
```python
from langchain.llms import VertexAI
from langchain.chains import LLMChain
import time
from typing import Optional

class DynamicPromptOptimizer:
    def __init__(self, model_name="gemini-pro"):
        self.llm = VertexAI(model_name=model_name)
        self.performance_history = []
        
    def optimize_for_task(self, task_type: str, complexity: str, 
                         creativity_level: str) -> Dict[str, Any]:
        """작업 유형에 따른 최적 설정 추천"""
        
        config_map = {
            ("classification", "low", "low"): {
                "temperature": 0.1,
                "max_tokens": 50,
                "top_k": 20,
                "top_p": 0.9,
                "style": "정확하고 간결하게"
            },
            ("creative", "high", "high"): {
                "temperature": 0.8,
                "max_tokens": 1024,
                "top_k": 40,
                "top_p": 0.95,
                "style": "창의적이고 다양하게"
            },
            ("analysis", "medium", "low"): {
                "temperature": 0.3,
                "max_tokens": 512,
                "top_k": 30,
                "top_p": 0.9,
                "style": "논리적이고 체계적으로"
            }
        }
        
        key = (task_type, complexity, creativity_level)
        return config_map.get(key, config_map[("analysis", "medium", "low")])
    
    def create_adaptive_prompt(self, base_task: str, context: Optional[str] = None, 
                             examples: Optional[List[Dict]] = None,
                             output_format: str = "자유 형식") -> str:
        """상황에 맞는 적응형 프롬프트 생성"""
        
        prompt_parts = []
        
        # 1. 역할 및 맥락 설정
        if context:
            prompt_parts.append(f"맥락: {context}")
        
        # 2. 작업 정의 (명확하고 구체적으로)
        prompt_parts.append(f"작업: {base_task}")
        
        # 3. 예시 추가 (가능한 경우)
        if examples:
            prompt_parts.append("예시:")
            for i, example in enumerate(examples, 1):
                input_text = example.get('input', example.get('question', ''))
                output_text = example.get('output', example.get('answer', ''))
                prompt_parts.append(f"{i}. 입력: {input_text}")
                prompt_parts.append(f"   출력: {output_text}")
        
        # 4. 출력 형식 명시
        if output_format != "자유 형식":
            prompt_parts.append(f"출력 형식: {output_format}")
        
        # 5. 입력 placeholder
        prompt_parts.append("입력: {input}")
        prompt_parts.append("출력:")
        
        return "\n\n".join(prompt_parts)
    
    def test_prompt_variants(self, base_prompt: str, test_inputs: List[str], 
                           variations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """프롬프트 변형들의 성능 테스트"""
        
        results = {}
        
        for i, variation in enumerate(variations):
            variant_name = f"variant_{i+1}"
            variant_results = []
            
            # LLM 설정 적용
            llm = VertexAI(
                model_name="gemini-pro",
                temperature=variation.get('temperature', 0.3),
                max_output_tokens=variation.get('max_tokens', 1024),
                top_k=variation.get('top_k', 30),
                top_p=variation.get('top_p', 0.9)
            )
            
            # 프롬프트 수정
            modified_prompt = base_prompt
            if 'style_instruction' in variation:
                modified_prompt += f"\n\n스타일: {variation['style_instruction']}"
            
            prompt_template = PromptTemplate(
                input_variables=["input"],
                template=modified_prompt
            )
            
            chain = LLMChain(llm=llm, prompt=prompt_template)
            
            # 테스트 실행
            for test_input in test_inputs:
                start_time = time.time()
                try:
                    response = chain.run(input=test_input)
                    execution_time = time.time() - start_time
                    
                    variant_results.append({
                        "input": test_input,
                        "output": response,
                        "execution_time": execution_time,
                        "success": True
                    })
                except Exception as e:
                    variant_results.append({
                        "input": test_input,
                        "error": str(e),
                        "execution_time": time.time() - start_time,
                        "success": False
                    })
            
            # 성능 지표 계산
            success_rate = sum(1 for r in variant_results if r['success']) / len(variant_results)
            avg_time = sum(r['execution_time'] for r in variant_results) / len(variant_results)
            
            results[variant_name] = {
                "variation": variation,
                "success_rate": success_rate,
                "avg_execution_time": avg_time,
                "detailed_results": variant_results
            }
        
        return results

# 사용 예시
optimizer = DynamicPromptOptimizer()

# 최적 설정 추천
optimal_config = optimizer.optimize_for_task("classification", "low", "low")
print(f"권장 설정: {optimal_config}")

# 적응형 프롬프트 생성
adaptive_prompt = optimizer.create_adaptive_prompt(
    base_task="고객 문의를 카테고리별로 분류",
    context="전자제품 쇼핑몰 고객 서비스",
    examples=[
        {"input": "배송이 언제 오나요?", "output": "배송문의"},
        {"input": "환불하고 싶어요", "output": "환불문의"},
        {"input": "제품이 고장났어요", "output": "기술지원"}
    ],
    output_format="카테고리명만 반환"
)

# 프롬프트 변형 테스트
variations = [
    {"temperature": 0.1, "style_instruction": "정확하고 간결하게"},
    {"temperature": 0.3, "style_instruction": "친근하고 도움이 되도록"},
    {"temperature": 0.0, "max_tokens": 10}  # 초정확 모드
]

test_inputs = [
    "언제 배송되나요?",
    "색상 변경 가능한가요?",
    "AS 센터 위치가 어디인가요?"
]

test_results = optimizer.test_prompt_variants(
    adaptive_prompt, test_inputs, variations
)

# 최고 성능 변형 선택
best_variant = max(test_results.items(), key=lambda x: x[1]['success_rate'])
print(f"최고 성능 변형: {best_variant[0]} (성공률: {best_variant[1]['success_rate']:.2%})")
```

### 🎯 **Gemini API 최적화 활용**

#### JSON 복구 및 스키마 검증 시스템
```python
import json
import jsonschema
from typing import Dict, Any, Optional
import re

class JSONOutputManager:
    def __init__(self):
        self.repair_patterns = [
            (r'}\s*$', '}'),  # 마지막 중괄호 정리
            (r',\s*}', '}'),  # 마지막 콤마 제거
            (r',\s*]', ']'),  # 배열 마지막 콤마 제거
        ]
    
    def repair_json(self, json_string: str) -> Optional[str]:
        """불완전한 JSON 복구"""
        try:
            # 1. 기본 파싱 시도
            json.loads(json_string)
            return json_string
        except json.JSONDecodeError:
            pass
        
        # 2. 일반적인 패턴 수정
        cleaned = json_string.strip()
        
        # 3. 일반적인 수정 패턴 적용
        for pattern, replacement in self.repair_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)
        
        # 4. 중괄호/대괄호 매칭 확인 및 보완
        open_braces = cleaned.count('{')
        close_braces = cleaned.count('}')
        
        if open_braces > close_braces:
            cleaned += '}' * (open_braces - close_braces)
        
        open_brackets = cleaned.count('[')
        close_brackets = cleaned.count(']')
        
        if open_brackets > close_brackets:
            cleaned += ']' * (open_brackets - close_brackets)
        
        # 5. 최종 검증
        try:
            json.loads(cleaned)
            return cleaned
        except json.JSONDecodeError:
            return None
    
    def validate_against_schema(self, json_ Dict[str, Any], 
                              schema: Dict[str, Any]) -> Dict[str, Any]:
        """스키마 기반 JSON 검증"""
        try:
            jsonschema.validate(instance=json_data, schema=schema)
            return {"valid": True, "errors": []}
        except jsonschema.ValidationError as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "path": list(e.absolute_path) if e.absolute_path else []
            }
    
    def create_schema_prompt(self, schema: Dict[str, Any], task: str) -> str:
        """스키마 기반 프롬프트 생성"""
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        
        return f"""
작업: {task}

출력 스키마 (반드시 준수):
```
{schema_str}
```

중요 지침:
1. 스키마의 모든 필수 필드를 포함하세요
2. 데이터 타입을 정확히 맞춰주세요
3. 추가 텍스트 없이 JSON만 반환하세요
4. 유효한 JSON 형식을 보장하세요

입력: {{input}}

JSON 출력:
"""

# 사용 예시
json_manager = JSONOutputManager()

# 제품 분석 스키마 정의
product_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "category": {"type": "string"},
        "sentiment": {"type": "string", "enum": ["POSITIVE", "NEUTRAL", "NEGATIVE"]},
        "price_range": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
        "features": {
            "type": "array",
            "items": {"type": "string"}
        },
        "rating": {"type": "number", "minimum": 1, "maximum": 5}
    },
    "required": ["name", "category", "sentiment", "rating"]
}

# 스키마 기반 프롬프트 생성
schema_prompt = json_manager.create_schema_prompt(
    product_schema, 
    "제품 리뷰를 분석하여 구조화된 정보를 추출"
)

# JSON 복구 테스트
broken_json = '{"name": "iPhone", "category": "스마트폰", "sentiment": "POSITIVE"'
repaired = json_manager.repair_json(broken_json)
print(f"복구된 JSON: {repaired}")
```

#### 프롬프트 문서화 및 버전 관리 시스템
```python
import datetime
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class PromptAttempt:
    """프롬프트 시도 기록"""
    name: str
    version: str
    goal: str
    model: str
    temperature: float
    token_limit: int
    top_k: Optional[int]
    top_p: float
    prompt_text: str
    test_inputs: List[str]
    outputs: List[str]
    success_rate: float
    avg_execution_time: float
    feedback: str
    timestamp: datetime.datetime
    hyperlink: Optional[str] = None

class PromptDocumentationSystem:
    def __init__(self):
        self.attempts: List[PromptAttempt] = []
        self.performance_trends = {}
    
    def log_attempt(self, attempt: PromptAttempt):
        """프롬프트 시도 로깅"""
        self.attempts.append(attempt)
        
        # 성능 트렌드 업데이트
        prompt_name = attempt.name
        if prompt_name not in self.performance_trends:
            self.performance_trends[prompt_name] = []
        
        self.performance_trends[prompt_name].append({
            'version': attempt.version,
            'success_rate': attempt.success_rate,
            'timestamp': attempt.timestamp
        })
    
    def get_best_performing_version(self, prompt_name: str) -> Optional[PromptAttempt]:
        """최고 성능 버전 조회"""
        relevant_attempts = [a for a in self.attempts if a.name == prompt_name]
        if not relevant_attempts:
            return None
        
        return max(relevant_attempts, key=lambda x: x.success_rate)
    
    def export_to_csv(self, filename: str):
        """CSV로 내보내기"""
        data = []
        for attempt in self.attempts:
            data.append({
                'Name': attempt.name,
                'Version': attempt.version,
                'Goal': attempt.goal,
                'Model': attempt.model,
                'Temperature': attempt.temperature,
                'Token_Limit': attempt.token_limit,
                'Top_K': attempt.top_k,
                'Top_P': attempt.top_p,
                'Success_Rate': attempt.success_rate,
                'Avg_Execution_Time': attempt.avg_execution_time,
                'Feedback': attempt.feedback,
                'Timestamp': attempt.timestamp,
                'Hyperlink': attempt.hyperlink
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    def generate_performance_report(self, prompt_name: str) -> Dict[str, Any]:
        """성능 보고서 생성"""
        relevant_attempts = [a for a in self.attempts if a.name == prompt_name]
        
        if not relevant_attempts:
            return {"error": "해당 프롬프트에 대한 기록이 없습니다."}
        
        # 성능 통계
        success_rates = [a.success_rate for a in relevant_attempts]
        execution_times = [a.avg_execution_time for a in relevant_attempts]
        
        return {
            "total_attempts": len(relevant_attempts),
            "avg_success_rate": sum(success_rates) / len(success_rates),
            "best_success_rate": max(success_rates),
            "worst_success_rate": min(success_rates),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "improvement_trend": self._calculate_trend(relevant_attempts),
            "latest_version": max(relevant_attempts, key=lambda x: x.timestamp).version,
            "best_version": max(relevant_attempts, key=lambda x: x.success_rate).version
        }
    
    def _calculate_trend(self, attempts: List[PromptAttempt]) -> str:
        """성능 트렌드 계산"""
        if len(attempts) < 2:
            return "데이터 부족"
        
        sorted_attempts = sorted(attempts, key=lambda x: x.timestamp)
        first_half = sorted_attempts[:len(sorted_attempts)//2]
        second_half = sorted_attempts[len(sorted_attempts)//2:]
        
        first_avg = sum(a.success_rate for a in first_half) / len(first_half)
        second_avg = sum(a.success_rate for a in second_half) / len(second_half)
        
        if second_avg > first_avg + 0.05:
            return "상승"
        elif second_avg < first_avg - 0.05:
            return "하락"
        else:
            return "안정"

# 프롬프트 A/B 테스트 시스템
class PromptABTester:
    def __init__(self, doc_system: PromptDocumentationSystem):
        self.doc_system = doc_system
    
    def run_ab_test(self, prompt_a: str, prompt_b: str, test_cases: List[Dict],
                   model_config: Dict, test_name: str) -> Dict[str, Any]:
        """A/B 테스트 실행"""
        
        results = {"prompt_a": [], "prompt_b": []}
        
        # 프롬프트 A 테스트
        for case in test_cases:
            # 실제 LLM 호출 시뮬레이션
            success_a = self._simulate_llm_call(prompt_a, case, model_config)
            results["prompt_a"].append(success_a)
        
        # 프롬프트 B 테스트
        for case in test_cases:
            success_b = self._simulate_llm_call(prompt_b, case, model_config)
            results["prompt_b"].append(success_b)
        
        # 통계 계산
        success_rate_a = sum(results["prompt_a"]) / len(results["prompt_a"])
        success_rate_b = sum(results["prompt_b"]) / len(results["prompt_b"])
        
        # 결과 기록
        self._log_ab_results(test_name, prompt_a, prompt_b, 
                           success_rate_a, success_rate_b, model_config)
        
        return {
            "test_name": test_name,
            "prompt_a_success_rate": success_rate_a,
            "prompt_b_success_rate": success_rate_b,
            "winner": "A" if success_rate_a > success_rate_b else "B",
            "improvement": abs(success_rate_a - success_rate_b),
            "statistical_significance": self._calculate_significance(
                results["prompt_a"], results["prompt_b"]
            )
        }
    
    def _simulate_llm_call(self, prompt: str, test_case: Dict, config: Dict) -> bool:
        """LLM 호출 시뮬레이션 (실제 구현에서는 진짜 LLM 호출)"""
        # 여기서는 간단한 시뮬레이션
        import random
        return random.random() > 0.3  # 70% 성공률 가정
    
    def _log_ab_results(self, test_name: str, prompt_a: str, prompt_b: str,
                       success_a: float, success_b: float, config: Dict):
        """A/B 테스트 결과 로깅"""
        
        timestamp = datetime.datetime.now()
        
        # 프롬프트 A 기록
        attempt_a = PromptAttempt(
            name=f"{test_name}_A",
            version="1.0",
            goal="A/B 테스트",
            model=config.get("model", "gemini-pro"),
            temperature=config.get("temperature", 0.3),
            token_limit=config.get("token_limit", 1024),
            top_k=config.get("top_k"),
            top_p=config.get("top_p", 0.9),
            prompt_text=prompt_a,
            test_inputs=[],
            outputs=[],
            success_rate=success_a,
            avg_execution_time=0.0,
            feedback=f"A/B 테스트 결과: {'승리' if success_a > success_b else '패배'}",
            timestamp=timestamp
        )
        
        # 프롬프트 B 기록
        attempt_b = PromptAttempt(
            name=f"{test_name}_B",
            version="1.0",
            goal="A/B 테스트",
            model=config.get("model", "gemini-pro"),
            temperature=config.get("temperature", 0.3),
            token_limit=config.get("token_limit", 1024),
            top_k=config.get("top_k"),
            top_p=config.get("top_p", 0.9),
            prompt_text=prompt_b,
            test_inputs=[],
            outputs=[],
            success_rate=success_b,
            avg_execution_time=0.0,
            feedback=f"A/B 테스트 결과: {'승리' if success_b > success_a else '패배'}",
            timestamp=timestamp
        )
        
        self.doc_system.log_attempt(attempt_a)
        self.doc_system.log_attempt(attempt_b)
    
    def _calculate_significance(self, results_a: List[bool], 
                              results_b: List[bool]) -> str:
        """통계적 유의성 계산 (간단한 버전)"""
        if len(results_a) < 30 or len(results_b) < 30:
            return "표본 크기 부족"
        
        success_a = sum(results_a) / len(results_a)
        success_b = sum(results_b) / len(results_b)
        
        difference = abs(success_a - success_b)
        
        if difference > 0.1:
            return "통계적으로 유의미"
        elif difference > 0.05:
            return "보통 수준의 차이"
        else:
            return "유의미한 차이 없음"

# 사용 예시
doc_system = PromptDocumentationSystem()
ab_tester = PromptABTester(doc_system)

# 프롬프트 시도 기록
attempt = PromptAttempt(
    name="sentiment_classifier",
    version="1.0",
    goal="고객 리뷰 감정 분석",
    model="gemini-pro",
    temperature=0.1,
    token_limit=50,
    top_k=20,
    top_p=0.9,
    prompt_text="다음 리뷰의 감정을 분류하세요: {review}",
    test_inputs=["좋아요", "나쁘네요", "그냥 그래요"],
    outputs=["POSITIVE", "NEGATIVE", "NEUTRAL"],
    success_rate=0.85,
    avg_execution_time=1.2,
    feedback="전반적으로 좋은 성능",
    timestamp=datetime.datetime.now()
)

doc_system.log_attempt(attempt)

# A/B 테스트 실행
test_cases = [
    {"input": "이 제품 정말 좋아요!", "expected": "POSITIVE"},
    {"input": "별로에요", "expected": "NEGATIVE"}
]

ab_result = ab_tester.run_ab_test(
    prompt_a="감정을 분류하세요: {input}",
    prompt_b="다음 텍스트의 감정을 POSITIVE, NEGATIVE, NEUTRAL 중 하나로 분류하세요: {input}",
    test_cases=test_cases,
    model_config={"model": "gemini-pro", "temperature": 0.1},
    test_name="sentiment_comparison"
)

print(f"A/B 테스트 결과: {ab_result}")

# 성능 보고서 생성
report = doc_system.generate_performance_report("sentiment_classifier")
print(f"성능 보고서: {report}")

# CSV 내보내기
doc_system.export_to_csv("prompt_attempts.csv")
```

### 📊 **작업별 최적화 가이드**

| 작업 유형 | Temperature | Max Tokens | 권장 기법 | 주의사항 |
|-----------|-------------|------------|-----------|----------|
| 분류 | 0.0-0.1 | 10-50 | Few-shot + 예시 섞기 | 클래스 균형 |
| 요약 | 0.1-0.3 | 200-500 | 구조화된 지시사항 | 길이 제한 명시 |
| 생성 | 0.7-0.9 | 1024-2048 | 역할 프롬프팅 | 창의성과 일관성 균형 |
| 추출 | 0.0-0.2 | 100-300 | JSON 스키마 활용 | 정확한 형식 지정 |
| 번역 | 0.1-0.3 | 원문의 1.5배 | 맥락 제공 | 문화적 뉘앙스 고려 |

### 🔄 **지속적 개선 프로세스**
```python
class ContinuousImprovementSystem:
    def __init__(self):
        self.feedback_loop = []
        self.performance_baseline = {}
    
    def establish_baseline(self, prompt_name: str, initial_performance: Dict):
        """성능 기준선 설정"""
        self.performance_baseline[prompt_name] = {
            'initial_success_rate': initial_performance['success_rate'],
            'initial_speed': initial_performance['avg_time'],
            'established_date': datetime.datetime.now()
        }
    
    def track_performance_drift(self, prompt_name: str, 
                              current_performance: Dict) -> Dict[str, Any]:
        """성능 변화 추적"""
        if prompt_name not in self.performance_baseline:
            return {"error": "기준선이 설정되지 않았습니다"}
        
        baseline = self.performance_baseline[prompt_name]
        
        success_drift = current_performance['success_rate'] - baseline['initial_success_rate']
        speed_drift = current_performance['avg_time'] - baseline['initial_speed']
        
        return {
            "success_rate_drift": success_drift,
            "speed_drift": speed_drift,
            "needs_optimization": abs(success_drift) > 0.1 or speed_drift > 2.0,
            "recommendation": self._generate_optimization_recommendation(
                success_drift, speed_drift
            )
        }
    
    def _generate_optimization_recommendation(self, success_drift: float, 
                                           speed_drift: float) -> str:
        """최적화 권장사항 생성"""
        if success_drift < -0.1:
            return "성능 저하 감지: 프롬프트 재검토 및 예시 업데이트 필요"
        elif speed_drift > 2.0:
            return "응답 속도 저하: 토큰 길이 줄이기 또는 Temperature 낮추기"
        elif success_drift > 0.1:
            return "성능 향상 확인: 현재 설정 유지 권장"
        else:
            return "안정적 성능: 정기 모니터링 지속"

# 실무 체크리스트 생성기
class PracticalChecklistGenerator:
    @staticmethod
    def generate_prompt_checklist() -> List[str]:
        """프롬프트 작성 체크리스트"""
        return [
            "✅ 명확하고 구체적인 작업 정의",
            "✅ 적절한 예시 제공 (3-5개)",
            "✅ 원하는 출력 형식 명시",
            "✅ 역할 또는 맥락 설정",
            "✅ 제약사항보다 지시사항 우선",
            "✅ 변수 활용으로 재사용성 확보",
            "✅ 온도 설정 최적화",
            "✅ 토큰 길이 적절히 제한",
            "✅ 테스트 케이스 준비",
            "✅ 성능 측정 방법 정의"
        ]
    
    @staticmethod
    def generate_testing_checklist() -> List[str]:
        """프롬프트 테스트 체크리스트"""
        return [
            "✅ 다양한 입력으로 테스트",
            "✅ 경계 사례(edge case) 확인",
            "✅ 일관성 검증 (여러 번 실행)",
            "✅ 성능 지표 측정",
            "✅ 오류 처리 확인",
            "✅ 출력 형식 검증",
            "✅ 편향성 체크",
            "✅ 안전성 검토",
            "✅ 비용 대비 효과 분석",
            "✅ 사용자 피드백 수집"
        ]

# 사용 예시
improvement_system = ContinuousImprovementSystem()
checklist_gen = PracticalChecklistGenerator()

# 기준선 설정
improvement_system.establish_baseline(
    "customer_inquiry_classifier",
    {"success_rate": 0.85, "avg_time": 1.5}
)

# 성능 드리프트 확인
drift_result = improvement_system.track_performance_drift(
    "customer_inquiry_classifier",
    {"success_rate": 0.78, "avg_time": 2.1}
)

print(f"성능 변화 분석: {drift_result}")

# 체크리스트 출력
print("\n=== 프롬프트 작성 체크리스트 ===")
for item in checklist_gen.generate_prompt_checklist():
    print(item)

print("\n=== 프롬프트 테스트 체크리스트 ===")
for item in checklist_gen.generate_testing_checklist():
    print(item)
```

### 💡 **실무 팁 정리**

#### 🚀 **효율성 향상**
- **템플릿 재사용**: 성공한 프롬프트 패턴을 템플릿화하여 재활용
- **배치 처리**: 유사한 작업들을 한 번에 처리하여 비용 절약
- **캐싱 활용**: 반복적인 쿼리 결과를 캐싱하여 응답 속도 향상

#### 🎯 **품질 보장**
- **다단계 검증**: 출력 형식 → 내용 정확성 → 편향성 순으로 검증
- **사용자 피드백 루프**: 실제 사용자 피드백을 프롬프트 개선에 반영
- **정기적 성능 리뷰**: 모델 업데이트나 데이터 변화에 따른 성능 변화 모니터링

#### 📈 **확장성 고려**
- **모듈화된 프롬프트**: 큰 작업을 작은 단위로 분할하여 관리
- **다국어 지원**: 언어별 특성을 고려한 프롬프트 변형 준비
- **플랫폼 독립성**: 특정 모델에 종속되지 않는 일반화된 프롬프트 설계

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)