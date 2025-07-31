# 📘 03. 기본 프롬프팅 기법 (Basic Prompting Techniques)

## 핵심 요약
- **Zero-shot 프롬프팅**은 예시 없이 작업 설명만으로 결과를 얻는 가장 간단한 형태의 프롬프트
- **One-shot과 Few-shot 프롬프팅**은 1개 또는 여러 개의 예시를 제공하여 모델이 원하는 패턴을 학습하도록 유도
- **예시의 품질**이 결과를 좌우하며, 다양하고 고품질의 예시를 제공하는 것이 중요
- **복잡한 작업일수록** 더 많은 예시(3-5개)가 필요하며, 모델의 입력 길이 제한을 고려해야 함

---

## 주요 개념과 설명

### 🎯 **Zero-shot 프롬프팅**
- **정의**: 예시 없이 작업 설명만으로 LLM에게 태스크를 요청하는 방식
- **장점**: 간단하고 빠르며, 추가 예시 준비 불필요
- **단점**: 복잡한 작업이나 특정 출력 형식이 필요할 때 제한적
- **적용 분야**: 질문 답변, 간단한 분류, 번역 등

### 🔗 **One-shot 프롬프팅**
- **정의**: 하나의 예시를 제공하여 모델이 모방할 수 있도록 하는 방식
- **효과**: 출력 구조나 패턴을 명확히 제시할 때 유용
- **사용 시기**: 특정 형식이나 스타일을 원할 때

### 📚 **Few-shot 프롬프팅**
- **정의**: 여러 개의 예시(보통 3-5개)를 제공하여 패턴을 학습시키는 방식
- **권장 개수**: 최소 3-5개, 복잡한 작업은 더 많이 필요할 수 있음
- **패턴 인식**: 여러 예시를 통해 모델이 일관된 패턴을 파악

---

## 프롬프트 예시

### Zero-shot 영화 리뷰 분류
```plaintext
# 기본 Zero-shot 예시
작업: 영화 리뷰를 POSITIVE, NEUTRAL, NEGATIVE로 분류

리뷰: "Her"는 AI가 계속 진화하도록 허용할 경우 인류가 향하고 있는 방향을 
보여주는 충격적인 연구입니다. 이런 걸작 같은 영화가 더 많았으면 좋겠습니다.

감정:
```
**출력**: `POSITIVE`

### Few-shot 피자 주문 파싱
```plaintext
# Few-shot JSON 파싱 예시
고객의 피자 주문을 유효한 JSON으로 파싱하세요:

예시 1:
입력: 치즈, 토마토 소스, 페퍼로니가 들어간 스몰 피자를 원합니다.
JSON 응답:
```
{
  "size": "small",
  "type": "normal", 
  "ingredients": ["cheese", "tomato sauce", "pepperoni"]
}
```

예시 2:
입력: 토마토 소스, 바질, 모짜렐라가 들어간 라지 피자 주세요.
JSON 응답:
```
{
  "size": "large",
  "type": "normal",
  "ingredients": ["tomato sauce", "basil", "mozzarella"]
}
```

이제 파싱해주세요:
입력: 라지 피자로, 반은 치즈와 모짜렐라, 나머지 반은 토마토 소스, 햄, 파인애플 넣어주세요.
JSON 응답:
```

**출력**:
```json
{
  "size": "large",
  "type": "half-half",
  "ingredients": [["cheese", "mozzarella"], ["tomato sauce", "ham", "pineapple"]]
}
```

---

## 활용 팁

### 🚀 **LangChain에서의 Zero-shot 구현**
```python
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.chains import LLMChain

# Zero-shot 분류 템플릿
zero_shot_template = """
작업: {task}

입력: {input}
출력:"""

prompt = PromptTemplate(
    input_variables=["task", "input"],
    template=zero_shot_template
)

llm = VertexAI(model_name="gemini-pro", temperature=0.1)
chain = LLMChain(llm=llm, prompt=prompt)

# 실행
result = chain.run(
    task="텍스트를 긍정/부정/중립으로 분류",
    input="이 영화는 정말 훌륭했습니다!"
)
```

### 📚 **Few-shot 체인 구성**
```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# 예시 정의
examples = [
    {
        "input": "작은 피자에 치즈와 페퍼로니 넣어주세요",
        "output": '{"size": "small", "toppings": ["cheese", "pepperoni"]}'
    },
    {
        "input": "큰 피자에 토마토소스와 바질 넣어주세요", 
        "output": '{"size": "large", "toppings": ["tomato sauce", "basil"]}'
    }
]

# 예시 템플릿
example_template = """
입력: {input}
출력: {output}"""

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template=example_template
)

# Few-shot 프롬프트 구성
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="피자 주문을 JSON으로 변환하세요:\n\n",
    suffix="\n입력: {input}\n출력:",
    input_variables=["input"]
)

chain = LLMChain(llm=llm, prompt=few_shot_prompt)
```

### 🎯 **Gemini API Few-shot 활용**
```python
import vertexai
from vertexai.generative_models import GenerativeModel

def create_few_shot_prompt(examples, new_input):
    """Few-shot 프롬프트 생성"""
    prompt = "다음 예시들을 참고하여 패턴을 학습하고 새로운 입력을 처리하세요:\n\n"
    
    for i, example in enumerate(examples, 1):
        prompt += f"예시 {i}:\n"
        prompt += f"입력: {example['input']}\n"
        prompt += f"출력: {example['output']}\n\n"
    
    prompt += f"새로운 입력: {new_input}\n출력:"
    return prompt

# 사용 예시
examples = [
    {"input": "안녕하세요", "output": "Hello"},
    {"input": "감사합니다", "output": "Thank you"},
    {"input": "죄송합니다", "output": "I'm sorry"}
]

model = GenerativeModel("gemini-pro")
prompt = create_few_shot_prompt(examples, "좋은 하루 되세요")
response = model.generate_content(prompt)
```

### 📋 **예시 선택 가이드라인**

#### 🎯 **좋은 예시의 특징**
```python
# 품질 높은 예시 세트
good_examples = [
    {
        "input": "이 영화는 정말 재미있고 감동적이었습니다.",
        "output": "POSITIVE",
        "reason": "명확한 긍정 표현"
    },
    {
        "input": "그냥 그런 영화였어요. 특별할 게 없네요.",
        "output": "NEUTRAL", 
        "reason": "중립적 표현"
    },
    {
        "input": "시간 낭비였습니다. 정말 지루했어요.",
        "output": "NEGATIVE",
        "reason": "명확한 부정 표현"
    }
]
```

#### ❌ **피해야 할 예시**
```python
# 문제가 있는 예시들
bad_examples = [
    {
        "input": "영화가 좋았는데 나빴어요",  # 모순된 표현
        "output": "POSITIVE",  # 잘못된 분류
        "issue": "혼란스러운 입력"
    },
    {
        "input": "ㅎㅎㅎ 개웃김 ㅋㅋㅋ",  # 인터넷 슬랭
        "output": "POSITIVE",
        "issue": "일관성 없는 언어 스타일"
    }
]
```

### 🔄 **동적 Few-shot 예시 선택**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DynamicFewShotSelector:
    def __init__(self, example_pool):
        self.example_pool = example_pool
        self.vectorizer = TfidfVectorizer()
        self.example_vectors = self.vectorizer.fit_transform(
            [ex['input'] for ex in example_pool]
        )
    
    def select_examples(self, query, k=3):
        """쿼리와 가장 유사한 k개 예시 선택"""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.example_vectors)
        
        # 상위 k개 인덱스 선택
        top_indices = np.argsort(similarities[0])[-k:][::-1]
        
        return [self.example_pool[i] for i in top_indices]

# 사용법
selector = DynamicFewShotSelector(good_examples)
relevant_examples = selector.select_examples("이 영화는 최악이었습니다", k=2)
```

### 📊 **작업별 Few-shot 전략**

| 작업 유형 | 권장 예시 수 | 주의사항 | 최적 설정 |
|-----------|-------------|----------|-----------|
| 텍스트 분류 | 3-5개 | 클래스별 균등 배치 | Temperature: 0.1 |
| 데이터 추출 | 2-4개 | 다양한 입력 형식 | Temperature: 0.2 |
| 형식 변환 | 2-3개 | 정확한 출력 형식 | Temperature: 0.0 |
| 창작 작업 | 1-2개 | 스타일 일관성 | Temperature: 0.7 |

### 🔍 **Zero-shot vs Few-shot 선택 기준**
```python
def choose_prompting_strategy(task_complexity, format_specificity, data_available):
    """프롬프팅 전략 선택 도우미"""
    
    if task_complexity == "simple" and format_specificity == "low":
        return "zero_shot"
    elif format_specificity == "high" or task_complexity == "complex":
        if data_available >= 3:
            return "few_shot"
        else:
            return "one_shot" 
    else:
        return "few_shot"

# 사용 예시
strategy = choose_prompting_strategy(
    task_complexity="complex",
    format_specificity="high", 
    data_available=5
)
print(f"권장 전략: {strategy}")
```

### 📝 **프롬프트 성능 평가**
```python
def evaluate_prompting_performance(test_cases, prompt_template):
    """프롬프트 성능 평가"""
    correct = 0
    total = len(test_cases)
    
    for case in test_cases:
        result = model.generate_content(
            prompt_template.format(input=case['input'])
        )
        
        if result.text.strip() == case['expected']:
            correct += 1
    
    accuracy = correct / total
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total
    }

# A/B 테스트
zero_shot_results = evaluate_prompting_performance(test_cases, zero_shot_template)
few_shot_results = evaluate_prompting_performance(test_cases, few_shot_template)

print(f"Zero-shot 정확도: {zero_shot_results['accuracy']:.2%}")
print(f"Few-shot 정확도: {few_shot_results['accuracy']:.2%}")
```

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)
