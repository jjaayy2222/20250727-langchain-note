
## 📁 정리될 파일 구조

    ../google_prompt_guide_summary/
        ├── 01_introduction.md                      # 소개 및 프롬프트 엔지니어링 개념
        ├── 02_llm_output_configuration.md          # LLM 출력 설정 (Temperature, Top-K, Top-P)
        ├── 03_basic_prompting_techniques.md        # 기본 프롬프팅 기법 (Zero-shot, Few-shot)
        ├── 04_advanced_prompting_roles.md          # 고급 프롬프팅 (System, Role, Context)
        ├── 05_reasoning_techniques.md              # 추론 기법 (CoT, Self-consistency, ToT)
        ├── 06_action_techniques.md                 # 행동 기반 기법 (ReAct, APE)
        ├── 07_code_prompting.md                    # 코드 프롬프팅
        ├── 08_best_practices.md                    # 모범 사례 및 팁
        └── summary.md                          # 전체 요약

---
* 참고: [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)

<br>

# 📘 01. 소개 및 프롬프트 엔지니어링 개념

## 핵심 요약
- **프롬프트 엔지니어링**은 LLM이 정확한 출력을 생성하도록 고품질 프롬프트를 설계하는 과정[1]
- 모델, 훈련 데이터, 설정, 단어 선택, 스타일, 구조, 맥락이 모두 프롬프트 효과에 영향을 미침[1]
- **반복적 과정**이며, 부적절한 프롬프트는 모호하고 부정확한 응답을 야기할 수 있음[1]
- 데이터 사이언티스트나 ML 엔지니어가 아니어도 누구나 프롬프트를 작성할 수 있지만, 효과적인 프롬프트 작성은 복잡함[1]

---

## 주요 개념과 설명

### 🤖 **LLM 작동 원리**
- **예측 엔진**: 순차적 텍스트를 입력받아 다음 토큰을 예측[1]
- **토큰 기반**: 이전에 예측한 토큰을 텍스트 끝에 추가하여 다음 토큰을 계속 예측[1]
- **관계 기반 학습**: 이전 토큰들과 훈련 데이터에서 본 내용 간의 관계를 바탕으로 예측[1]

### 🎯 **프롬프트 엔지니어링의 목적**
- 텍스트 요약, 정보 추출, 질의응답, 텍스트 분류, 언어/코드 번역, 코드 생성, 문서화, 추론 등 다양한 작업 수행[1]

### 🔧 **프롬프트 최적화 요소**
- **모델 선택**: Gemini, GPT, Claude, Gemma, LLaMA 등 각 모델에 맞는 최적화 필요[1]
- **설정 조정**: Temperature, Top-K, Top-P 등 다양한 설정 조합[1]

---

## 프롬프트 예시

### 기본 프롬프트 구조
```plaintext
# 작업 정의
Classify movie reviews as POSITIVE, NEUTRAL or NEGATIVE.

# 입력 데이터  
Review: "Her" is a disturbing study revealing the direction 
umanity is headed if AI is allowed to keep evolving, 
unchecked. I wish there were more movies like this masterpiece.

# 출력 요청
Sentiment:
```

**출력**: `POSITIVE`[1]

---

## 활용 팁

### 🚀 **LangChain에서의 적용**
```python
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm                       # 또는 다른 LLM

# 템플릿 정의
template = """
작업: {task}
입력: {input_text}
출력 형식: {output_format}
 """

prompt = PromptTemplate(
    input_variables=["task", "input_text", "output_format"],
    template=template
)

# 체인 구성
llm = GooglePalm(temperature=0.1)
chain = LLMChain(llm=llm, prompt=prompt)
```

### 🎯 **Gemini API 활용 방법**
- **Vertex AI Studio**: 프롬프트 테스트 및 실험을 위한 플레이그라운드 활용[1]
- **API 직접 호출**: Temperature 등 세부 설정 제어 가능[1]
- **설정 최적화**: 작업 유형에 따른 Temperature, Top-K, Top-P 조정[1]

### 📋 **프롬프트 문서화 템플릿**
```markdown
| 항목 | 값 |
|------|-----|
| Name | 프롬프트_이름_버전 |
| Goal | 목표 한 줄 설명 |
| Model | gemini-pro |
| Temperature | 0.1 |
| Token Limit | 1024 |
| Top-K | 40 |
| Top-P | 0.8 |
| Prompt | 전체 프롬프트 내용 |
| Output | 실제 출력 결과 |
```

### 🔄 **반복적 개선 프로세스**

>> 1. **초기 프롬프트 작성** → 기본 요구사항 정의
>> 2. **테스트 및 평가** → 출력 품질 확인
>> 3. **설정 조정** → Temperature, 토큰 길이 등 최적화
>> 4. **프롬프트 개선** → 더 명확하고 구체적으로 수정
>> 5. **문서화** → 버전별 성능 기록

---

* 출처

  * [1] 22365_3_Prompt-Engineering_v7.pdf https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35543904/6dc0be28-e817-4723-a5f7-9b7b46cf1027/22365_3_Prompt-Engineering_v7.pdf
  * [2] Prompt Engineering | Kaggle https://www.kaggle.com/whitepaper-prompt-engineering
  * [3] Google dropped a 68-page prompt engineering guide, here's what's ... https://www.reddit.com/r/PromptEngineering/comments/1kggmh0/google_dropped_a_68page_prompt_engineering_guide/
  * [4] Google Prompt Engineering White Paper https://zero-ai.tistory.com/78
  * [5] Day 1 - Prompting - Kaggle https://www.kaggle.com/code/markishere/day-1-prompting
  * [6] Generative AI prompt samples - Google Cloud https://cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery
  * [7] [PDF] Prompt Engineering - Lee Boonstra - GPT AI Flow https://www.gptaiflow.tech/assets/files/2025-01-18-pdf-1-TechAI-Goolge-whitepaper_Prompt%20Engineering_v4-af36dcc7a49bb7269a58b1c9b89a8ae1.pdf
  * [8] 구글 프롬프트 엔지니어링 백서(Google Prompt Engineering ... https://eye-eye.tistory.com/53
  * [9] [LLM] Google Prompt Engineering Whiterpapers - 구글 프롬프트 ... https://mz-moonzoo.tistory.com/88
  * [10] AI-Powered PDF Summarizer and Quiz Generator - Kaggle https://www.kaggle.com/code/prabhatverma07/ai-powered-pdf-summarizer-and-quiz-generator
  * [11] 프롬프트 엔지니어링 문서 정리하기 - All I Need Is Data. - 티스토리 https://data-newbie.tistory.com/1029