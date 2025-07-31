# 📘 02. LLM 출력 설정 (LLM Output Configuration)

## 핵심 요약
- **출력 길이 제어**는 성능과 비용에 직접적인 영향을 미치며, 토큰 수가 많을수록 더 많은 계산 비용과 시간이 소요됨
- **Temperature, Top-K, Top-P**는 LLM의 창의성과 일관성을 조절하는 핵심 설정으로, 작업 유형에 따라 최적화가 필요
- **설정들의 상호작용**을 이해하고 조합하여 사용해야 하며, 극단적인 값 설정 시 다른 설정들이 무효화될 수 있음
- **반복 루프 버그** 방지를 위해 적절한 설정 균형을 맞춰야 함

---

## 주요 개념과 설명

### 🎯 **출력 길이 (Output Length)**
- **토큰 제한**: 응답에서 생성할 토큰 수를 제어
- **비용 영향**: 더 많은 토큰 = 더 높은 에너지 소비 + 느린 응답 + 높은 비용
- **주의사항**: 출력 길이 제한은 모델을 간결하게 만들지 않고, 단순히 토큰 한계에서 생성을 중단시킴

### 🌡️ **Temperature (온도)**
- **범위**: 0 (결정적) ~ 1+ (창의적)
- **0 설정**: 그리디 디코딩 - 가장 높은 확률의 토큰 선택
- **높은 값**: 더 다양하고 예측하기 어려운 결과
- **Softmax 함수**와 유사한 동작 원리

### 🎲 **Top-K 샘플링**
- **기능**: 상위 K개의 가능성 높은 토큰에서만 선택
- **높은 Top-K**: 더 창의적이고 다양한 출력
- **낮은 Top-K**: 더 제한적이고 사실적인 출력
- **K=1**: 그리디 디코딩과 동일

### 🎯 **Top-P 샘플링 (Nucleus Sampling)**
- **기능**: 누적 확률이 P값을 넘지 않는 토큰들에서 선택
- **범위**: 0 (그리디) ~ 1 (모든 토큰)
- **동적 선택**: 상황에 따라 선택되는 토큰 수가 변함

---

## 프롬프트 예시

### 기본 설정 조합
```plaintext
# 영화 리뷰 분류 - 창의성 불필요
Temperature: 0.1
Top-K: 20
Top-P: 0.9
Token Limit: 5

# 창의적 작업 - 스토리 생성
Temperature: 0.9
Top-K: 40
Top-P: 0.99
Token Limit: 1024

# 수학 문제 - 정확한 답 필요
Temperature: 0
Top-K: N/A (무관)
Top-P: N/A (무관)
```

### 설정별 비교 예시
```plaintext
프롬프트: "오늘 날씨가 좋아서"

# 낮은 창의성 (Temperature: 0.1)
→ "오늘 날씨가 좋아서 공원에 산책을 가기로 했습니다."

# 높은 창의성 (Temperature: 0.9)
→ "오늘 날씨가 좋아서 하늘을 나는 꿈을 꾸며 무지개 다리를 건넜습니다."
```

---

## 활용 팁

### 🚀 **LangChain에서의 설정 적용**

```python
from langchain.llms import VertexAI
from langchain.chat_models import ChatVertexAI

# 사실적 작업용 설정
factual_llm = VertexAI(
    model_name="gemini-pro",
    temperature=0.1,                            # temperature 낮게 설정
    max_output_tokens=256,
    top_k=20,
    top_p=0.9
)

# 창의적 작업용 설정
creative_llm = VertexAI(
    model_name="gemini-pro",
    temperature=0.8,                            # temperature 높게 설정
    max_output_tokens=1024,
    top_k=40,
    top_p=0.95
)

# 정확한 답변 필요한 작업
precise_llm = VertexAI(
    model_name="gemini-pro",
    temperature=0.0,                            # temperature = 0
    max_output_tokens=100
)
```

### 🎯 **Gemini API 직접 활용**

```python
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# 설정 객체 생성
config = GenerationConfig(
    temperature=0.2,
    top_p=0.95,
    top_k=30,
    max_output_tokens=1024,
)

# 모델 초기화
model = GenerativeModel(
    model_name="gemini-pro",
    generation_config=config
)

# 응답 생성
response = model.generate_content("프롬프트 내용")
```

### 📊 **작업별 권장 설정**

| 작업 유형 | Temperature | Top-K | Top-P | 설명 |
|-----------|-------------|-------|-------|------|
| 데이터 분류 | 0.0-0.1 | 20 | 0.9 | 일관된 정확한 분류 |
| 요약 | 0.1-0.3 | 30 | 0.9 | 사실적이지만 약간의 다양성 |
| 창작 | 0.7-0.9 | 40 | 0.99 | 높은 창의성과 다양성 |
| 코드 생성 | 0.1-0.3 | 30 | 0.95 | 정확하지만 다양한 접근법 |
| 수학 문제 | 0.0 | N/A | N/A | 정확한 단일 답 |

### ⚠️ **반복 루프 버그 방지**

```python
# 문제가 되는 설정 조합 피하기
# 1. 너무 낮은 Temperature + 높은 Top-K
# 2. 너무 높은 Temperature + 제한적인 Top-P

# 권장 안전 설정
safe_config = GenerationConfig(
    temperature=0.3,                    # 너무 극단적이지 않은 값
    top_p=0.95,                         # 적당한 다양성 허용
    top_k=30,                           # 중간 수준의 선택권
    max_output_tokens=512               # 적절한 길이 제한
)
```

### 🔄 **동적 설정 조정**

```python
def get_optimal_config(task_type: str) -> GenerationConfig:
    """작업 유형에 따른 최적 설정 반환"""
    
    configs = {
        "classification": GenerationConfig(
            temperature=0.1, top_k=20, top_p=0.9, max_output_tokens=10
        ),
        "creative_writing": GenerationConfig(
            temperature=0.8, top_k=40, top_p=0.99, max_output_tokens=1024
        ),
        "code_generation": GenerationConfig(
            temperature=0.2, top_k=30, top_p=0.95, max_output_tokens=2048
        ),
        "analysis": GenerationConfig(
            temperature=0.3, top_k=25, top_p=0.9, max_output_tokens=512
        )
    }
    
    return configs.get(task_type, configs["analysis"])

# 사용 예시
config = get_optimal_config("creative_writing")
model = GenerativeModel("gemini-pro", generation_config=config)
```

### 📝 **설정 실험 및 문서화**

```python
# 설정 실험을 위한 유틸리티
class ConfigExperiment:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.results = []
    
    def test_config(self, config: GenerationConfig, description: str):
        model = GenerativeModel("gemini-pro", generation_config=config)
        response = model.generate_content(self.prompt)
        
        self.results.append({
            "description": description,
            "config": config,
            "response": response.text,
            "token_count": response.usage_metadata.candidates_token_count
        })
    
    def compare_results(self):
        for result in self.results:
            print(f"설정: {result['description']}")
            print(f"응답: {result['response'][:100]}...")
            print(f"토큰 수: {result['token_count']}")
            print("-" * 50)

# 실험 실행
experiment = ConfigExperiment("창의적인 스토리를 써주세요.")
experiment.test_config(
    GenerationConfig(temperature=0.1, top_k=20, top_p=0.9),
    "보수적 설정"
)
experiment.test_config(
    GenerationConfig(temperature=0.8, top_k=40, top_p=0.99),
    "창의적 설정"
)
experiment.compare_results()
```

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)
