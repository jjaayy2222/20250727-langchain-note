# 📘 04. 고급 프롬프팅 - 시스템, 역할, 문맥 프롬프팅 (Advanced Prompting: System, Role & Contextual)

## 핵심 요약
- **System, Role, Contextual 프롬프팅**은 모두 LLM의 텍스트 생성을 안내하지만, 각각 다른 측면에 초점을 맞춤
- **System 프롬프팅**은 모델의 전반적인 맥락과 목적을 설정하여 기본적인 능력과 목표를 정의
- **Role 프롬프팅**은 모델에게 특정한 캐릭터나 정체성을 부여하여 일관된 응답 스타일과 전문성을 제공
- **Contextual 프롬프팅**은 현재 작업에 특정한 세부 정보와 배경 정보를 제공하여 응답의 정확성과 관련성을 향상

## 주요 개념과 설명

### 🔧 **System 프롬프팅 (System Prompting)**
- **목적**: 모델의 기본적인 능력과 전체적인 목표 정의
- **특징**: 출력 형식, 스타일, 구조에 대한 추가적인 요구사항 명시
- **활용**: 특정 형식(JSON, XML), 안전성 제어, 독성 방지 등
- **예시**: "영화 리뷰를 긍정/부정/중립으로만 분류하여 대문자로 반환"

### 🎭 **Role 프롬프팅 (Role Prompting)**
- **목적**: 모델에게 특정 역할이나 전문성을 부여
- **장점**: 일관된 어조, 스타일, 전문 지식을 가진 응답 생성
- **활용 분야**: 교육자, 여행 가이드, 컨설턴트, 코딩 도우미 등
- **스타일 옵션**: 대립적, 설명적, 직접적, 형식적, 유머러스, 영향력 있는, 비공식적, 영감을 주는, 설득적

### 📋 **Contextual 프롬프팅 (Contextual Prompting)**
- **목적**: 현재 대화나 작업과 관련된 구체적인 세부사항과 배경 정보 제공
- **특징**: 작업별로 동적이며 높은 특수성을 가짐
- **효과**: 모델의 요청 이해력 향상, 더 정확하고 관련성 높은 응답 생성

## 프롬프트 예시

### System 프롬프팅 - 기본 분류
```plaintext
# 시스템 설정
영화 리뷰를 긍정, 부정, 중립으로 분류합니다. 
결과는 대문자로만 반환하세요.

# 입력
리뷰: "Her"는 AI가 계속 진화할 경우 인류가 향하는 방향을 
보여주는 충격적인 연구입니다. 너무 충격적이어서 끝까지 볼 수 없었습니다.

감정:
```
**출력**: `NEGATIVE`

### System 프롬프팅 - JSON 형식
```plaintext
# 시스템 설정
영화 리뷰를 긍정, 부정, 중립으로 분류하고 유효한 JSON으로 반환하세요.

# 스키마
```
MOVIE: {
  "sentiment": String "POSITIVE" | "NEGATIVE" | "NEUTRAL",
  "name": String
}
```

# 입력
리뷰: "Her"는 AI가 계속 진화할 경우 인류가 향하는 방향을 
보여주는 충격적인 연구입니다. 너무 충격적이어서 끝까지 볼 수 없었습니다.

JSON 응답:
```
**출력**:
```json
{
  "sentiment": "NEGATIVE",
  "name": "Her"
}
```

### Role 프롬프팅 - 여행 가이드
```plaintext
# 역할 설정
당신은 여행 가이드입니다. 제가 위치를 알려드리면 
근처에서 방문할만한 3곳을 추천해주세요.

# 요청
저는 지금 암스테르담에 있고 박물관만 방문하고 싶습니다.

여행 제안:
```
**출력**:
1. **라익스뮤지엄**: 렘브란트의 "야경"을 포함한 네덜란드 걸작들로 유명한 세계적인 박물관
2. **반 고흐 뮤지엄**: "별이 빛나는 밤"과 "해바라기"를 포함한 반 고흐 작품의 최대 컬렉션
3. **스테델릭 현대미술관**: 피카소, 칸딘스키, 리트벨트 작품이 있는 현대 건축물의 현대미술관

### Role 프롬프팅 - 유머러스 스타일
```plaintext
# 역할 설정
유머러스한 스타일로 여행 가이드 역할을 해주세요. 
제가 위치를 알려드리면 근처에서 방문할만한 3곳을 추천해주세요.

# 요청
저는 지금 맨해튼에 있습니다.

여행 제안:
```
**출력**:
1. **엠파이어 스테이트 빌딩**: 거대한 바나나 없는 킹콩이 된 기분으로 맨해튼 스카이라인을 감상하세요
2. **모마(MoMA) 미술관**: 당신의 막대기 그림이 예술적 가치가 있는지 의문을 갖게 만드는 걸작들을 감상하세요
3. **5번가 쇼핑**: 지갑이 울게 만드는 디자이너 부티크에서 쇼핑하며 맨해튼의 화려함을 만끽하세요

### Contextual 프롬프팅 - 블로그 주제 제안
```plaintext
# 문맥 설정
맥락: 당신은 1980년대 레트로 아케이드 비디오 게임에 관한 블로그를 작성하고 있습니다.

# 요청
기사로 쓸 3가지 주제를 몇 줄의 설명과 함께 제안해주세요.

```
**출력**:
1. **아케이드 캐비닛 디자인의 진화**: 1970년대 목재와 금속 캐비닛부터 1980년대 네온 라이트가 있는 세련된 디자인까지의 변화 탐구
2. **80년대 아이코닉 아케이드 게임들**: 역사적 영향과 유산을 남긴 가장 상징적인 아케이드 게임들의 혁신과 인기 메커니즘 소개
3. **픽셀 아트의 부상과 레트로 부활**: 초기 아케이드 게임의 시각적 스타일로서 픽셀 아트의 진화와 현대 게임에서의 부활

## 활용 팁

### 🚀 **LangChain에서의 구현**

#### System 프롬프팅 구현
```python
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.chains import LLMChain

# System 프롬프트 템플릿
system_template = """
시스템 지시사항: {system_instruction}

작업: {task}
입력: {input}

{output_format}
"""

system_prompt = PromptTemplate(
    input_variables=["system_instruction", "task", "input", "output_format"],
    template=system_template
)

# JSON 출력을 위한 시스템 프롬프트
json_chain = LLMChain(
    llm=VertexAI(temperature=0.1),
    prompt=system_prompt
)

result = json_chain.run(
    system_instruction="영화 리뷰를 분류하고 JSON 형식으로 반환하세요.",
    task="감정 분석",
    input="이 영화는 정말 훌륭했습니다!",
    output_format='JSON 응답: {"sentiment": "...", "confidence": 0.95}'
)
```

#### Role 프롬프팅 구현
```python
from langchain.prompts import PromptTemplate

# Role 기반 프롬프트 템플릿
role_template = """
역할: {role}
스타일: {style}
전문 분야: {expertise}

{context}

요청: {request}
응답:"""

role_prompt = PromptTemplate(
    input_variables=["role", "style", "expertise", "context", "request"],
    template=role_template
)

# 여행 가이드 체인
travel_chain = LLMChain(llm=VertexAI(temperature=0.8), prompt=role_prompt)

result = travel_chain.run(
    role="경험이 풍부한 여행 가이드",
    style="친근하고 유머러스",
    expertise="유럽 문화 관광",
    context="고객은 3세 아이와 함께 여행 중",
    request="암스테르담에서 가족이 함께 즐길 수 있는 장소 3곳 추천"
)
```

#### Contextual 프롬프팅 구현
```python
# 동적 컨텍스트 관리 클래스
class ContextualPromptManager:
    def __init__(self):
        self.context_history = []
        
    def add_context(self, context_type: str, content: str):
        self.context_history.append({
            "type": context_type,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def build_contextual_prompt(self, current_request: str):
        context_str = "\n".join([
            f"{ctx['type']}: {ctx['content']}" 
            for ctx in self.context_history[-3:]  # 최근 3개 컨텍스트만 사용
        ])
        
        return f"""
배경 정보:
{context_str}

현재 요청: {current_request}

위 맥락을 고려하여 응답해주세요:"""

# 사용 예시
context_manager = ContextualPromptManager()
context_manager.add_context("프로젝트", "LangChain을 사용한 챗봇 개발")
context_manager.add_context("목표", "고객 문의 자동 응답 시스템 구축")
context_manager.add_context("제약사항", "한국어 지원 필수, JSON 형식 출력")

prompt = context_manager.build_contextual_prompt(
    "사용자 의도 분류를 위한 프롬프트 엔지니어링 방법을 알려주세요"
)
```

### 🎯 **Gemini API 활용**

#### 다중 프롬프팅 기법 결합
```python
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

class AdvancedPromptEngine:
    def __init__(self, model_name="gemini-pro"):
        self.model = GenerativeModel(model_name)
        
    def system_role_contextual_prompt(self, system_config, role_config, context_config, user_request):
        """System + Role + Contextual 프롬프팅 통합"""
        
        prompt = f"""
=== 시스템 설정 ===
{system_config['instruction']}
출력 형식: {system_config.get('format', '자유 형식')}
제약사항: {system_config.get('constraints', '없음')}

=== 역할 설정 ===
역할: {role_config['role']}
전문성: {role_config['expertise']}
어조: {role_config.get('tone', '전문적')}

=== 맥락 정보 ===
{context_config['background']}

=== 사용자 요청 ===
{user_request}

=== 응답 ===
"""
        
        config = GenerationConfig(
            temperature=system_config.get('temperature', 0.3),
            max_output_tokens=system_config.get('max_tokens', 1024)
        )
        
        response = self.model.generate_content(prompt, generation_config=config)
        return response.text

# 사용 예시
engine = AdvancedPromptEngine()

result = engine.system_role_contextual_prompt(
    system_config={
        'instruction': '코드 설명을 한국어로 제공하되, 초보자도 이해할 수 있게 작성',
        'format': '단계별 설명 + 코드 예시',
        'temperature': 0.2,
        'max_tokens': 1500
    },
    role_config={
        'role': '친절한 프로그래밍 강사',
        'expertise': 'Python, LangChain',
        'tone': '친근하고 설명적'
    },
    context_config={
        'background': 'LangChain을 처음 배우는 개발자를 위한 튜토리얼 제작 중'
    },
    user_request='LangChain의 PromptTemplate 사용법을 설명해주세요'
)
```

### 📊 **프롬프트 유형별 최적화 가이드**

| 프롬프트 유형 | 최적 Temperature | 권장 토큰 수 | 주요 활용 분야 |
|---------------|------------------|--------------|----------------|
| System | 0.0-0.2 | 50-200 | 분류, 변환, 형식화 |
| Role | 0.3-0.7 | 200-1000 | 창작, 상담, 교육 |
| Contextual | 0.2-0.5 | 300-1500 | 분석, 요약, 맞춤 응답 |
| 혼합 | 0.1-0.4 | 500-2000 | 복잡한 작업, 전문 서비스 |

### 🔄 **동적 프롬프트 선택 전략**
```python
class SmartPromptSelector:
    def __init__(self):
        self.prompt_strategies = {
            'classification': self._system_prompt,
            'creative': self._role_prompt,
            'analysis': self._contextual_prompt,
            'complex': self._hybrid_prompt
        }
    
    def select_strategy(self, task_type: str, complexity: str, creativity_needed: bool):
        """작업 특성에 따른 최적 프롬프트 전략 선택"""
        
        if task_type in ['classify', 'extract', 'format']:
            return 'classification'
        elif creativity_needed and complexity == 'low':
            return 'creative'
        elif complexity == 'high' and not creativity_needed:
            return 'analysis'
        else:
            return 'complex'
    
    def _system_prompt(self, **kwargs):
        return f"시스템 지시: {kwargs['task']}\n입력: {kwargs['input']}"
    
    def _role_prompt(self, **kwargs):
        return f"역할: {kwargs['role']}\n요청: {kwargs['request']}"
    
    def _contextual_prompt(self, **kwargs):
        return f"맥락: {kwargs['context']}\n분석 요청: {kwargs['request']}"
    
    def _hybrid_prompt(self, **kwargs):
        return f"""
시스템: {kwargs['system']}
역할: {kwargs['role']}  
맥락: {kwargs['context']}
요청: {kwargs['request']}
"""

# 사용 예시
selector = SmartPromptSelector()
strategy = selector.select_strategy('creative', 'medium', True)
```

### 🛡️ **안전성 및 품질 관리**
```python
class SafePromptValidator:
    def __init__(self):
        self.safety_checks = [
            self._check_harmful_content,
            self._check_bias_potential,
            self._validate_output_format
        ]
    
    def validate_prompt(self, prompt_text: str, expected_output_type: str):
        """프롬프트 안전성 및 품질 검증"""
        results = []
        
        for check in self.safety_checks:
            result = check(prompt_text, expected_output_type)
            results.append(result)
        
        return {
            'is_safe': all(r['passed'] for r in results),
            'issues': [r['issue'] for r in results if not r['passed']],
            'suggestions': [r['suggestion'] for r in results if r.get('suggestion')]
        }
    
    def _check_harmful_content(self, prompt, output_type):
        # 유해 콘텐츠 체크 로직
        return {'passed': True, 'issue': None}
    
    def _check_bias_potential(self, prompt, output_type):
        # 편향성 체크 로직
        return {'passed': True, 'issue': None}
    
    def _validate_output_format(self, prompt, expected_type):
        # 출력 형식 유효성 체크
        return {'passed': True, 'issue': None}

# 시스템에 안전성 검증 추가
validator = SafePromptValidator()
validation_result = validator.validate_prompt(prompt, 'json')

if validation_result['is_safe']:
    # 프롬프트 실행
    response = model.generate_content(prompt)
else:
    print(f"프롬프트 안전성 문제: {validation_result['issues']}")
```

---

* 출처
  * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)
