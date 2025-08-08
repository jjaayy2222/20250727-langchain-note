# LangChain Few-shot 프롬프트 고급 활용법

## 개요
Few-shot 프롬프트의 기본 개념을 넘어, 실제 프로덕션 환경에서 마주하는 문제점들과 해결 방법

## 1. Example Selector의 유사도 계산 문제와 해결

### 1-1. 기본 SemanticSimilarityExampleSelector의 한계

**문제 상황**: 
- `SemanticSimilarityExampleSelector`는 예시 전체(instruction + input + answer)를 벡터화하여 유사도 계산
- 결과적으로 사용자의 의도와 다른 예시가 선택되는 경우 발생

    ```<python>
        # 문제가 되는 기본 사용 사례
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples, 
            OpenAIEmbeddings(), 
            Chroma, 
            k=1
        )

        # "회의록 작성해 주세요" 요청
        question = {"instruction": "회의록을 작성해 주세요"}
        selected = example_selector.select_examples(question)
        # 결과: "문장 교정" 예시가 잘못 선택됨
    ```

### 1-2. Custom Example Selector를 통한 해결
- **핵심 아이디어**: instruction 필드에 가중치를 두어 작업 의도를 정확히 파악
 
    ```<python>
        from langchain_teddynote.prompts import CustomExampleSelector

        # 커스텀 선택기로 문제 해결
        custom_selector = CustomExampleSelector(examples, OpenAIEmbeddings())

        # 동일한 질문으로 테스트
        selected = custom_selector.select_examples({"instruction": "회의록을 작성해 주세요"})
        # 결과: 올바른 "회의록 작성" 예시 선택
    ```

**개선 효과**:
- "회의록 작성" → 회의록 예제 정확 선택 ✅
- "문서 요약" → 요약 예제 정확 선택 ✅
- "문장 교정" → 교정 예제 정확 선택 ✅

## 2. Vector Database 통합 아키텍처

### 2-1. Chroma DB + Embeddings 시스템
- 
    ```<python>
        # Vector DB 생성 및 임베딩 설정
        chroma = Chroma("fewshot_chat", OpenAIEmbeddings())

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),  # 의미적 유사성 측정
            chroma,             # 벡터 저장소
            k=1                 # 선택할 예시 개수
        )
    ```

### 2-2. 완성된 Few-shot Chain 구조
- 
    ```
        사용자 입력 → CustomExampleSelector → 관련 예시 선택 

        → FewShotChatMessagePromptTemplate → ChatPromptTemplate → LLM → 응답
    ```

## 3. JSON 응답 형식 처리

### 3-1. API 변경사항 대응

**변경된 올바른 구조**:

```<python>
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,                          # ChatPromptTemplate 객체 전달
        examples=examples
    )
```

### 3-2. 응답 형식 강제와 Few-shot의 상호작용

- `response_mime_type="application/json"` 설정 시
- Few-shot 예시가 JSON 형식을 강력하게 유도
- 결과: `temperature` 파라미터의 영향력 감소

## 4. 멀티태스크 Few-shot 실습 결과

### 4-1. 통합된 예시 세트
- 
    ```<python>
        examples = [
            {"instruction": "회의록 작성 전문가", "input": "...", "answer": "..."},
            {"instruction": "요약 전문가", "input": "...", "answer": "..."},  
            {"instruction": "문장 교정 전문가", "input": "...", "answer": "..."}
        ]
    ```

### 4-2. 실행 결과 분석

- **회의록 작성**: 체계적인 구조와 세부 항목으로 완성도 높은 결과
- **문서 요약**: 핵심 내용을 bullet point로 명확하게 정리
- **문장 교정**: 자연스러운 문장 개선과 격식체 변환

## 5. 확장성과 실무 적용

### 5-1. 예시 확장 전략
- 도메인별 예시 세트 구성 (기술문서, 비즈니스, 학술 등)
- 예시의 품질이 최종 결과에 미치는 영향이 매우 큼

### 5-2. 성능 최적화 포인트
- 예시 선택 정확도가 전체 시스템 성능의 핵심
- Vector DB 인덱싱 최적화로 검색 속도 개선 가능
