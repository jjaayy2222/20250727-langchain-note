# 🛠️ 02_Prompt/02_FewshotTemplates_2.ipynb 오류 해결 로그

> 작성일: 2025-08-08  
> 작성자: Jay  
---

## 1. `max_output_tokens`를 늘려도 결과가 동일하게 나오는 문제

### 1) 원인: 
- `seed 매개변수`가 활성화되어 모델의 `출력이 특정 값으로 고정`되었기 때문
- `max_output_tokens`는 최대 길이를 지정할 뿐, `seed`가 있는 한 내용은 변하지 않음

### 2) 문제 코드:

    ```<python>
        ChatGoogleGenerativeAI 객체에 seed를 고정하는 코드가 포함되어 있습니다.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.7,
            max_output_tokens=2048,
            model_kwargs={"seed": 42}                                # <-- seed로 인해 결과가 고정되었음
        )
    ```

### 3) 해결 코드:
- `seed 제거` or `주석 처리`하여 모델의 무작위성 허용

    ```<python>
        gemini_lc = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.7,                                        # 이제 이 값에 따라 결과가 달라짐
            max_output_tokens=2048,
            model_kwargs={}                                         # 빈 딕셔너리 처리 = seed 제거
        )
    ```

## 2. temperature 값을 변경해도 결과가 동일한 문제

### 1) 원인: 
- `Chroma 벡터스토어`가 `동일한 collection_name`을 사용하여 `캐싱된 예시`를 `계속 반환`했기 때문
- 이로 인해 모델은 항상 같은 예시를 참고하게 됨
  
### 2) 문제 코드:
- `collection_name`이 `고정된 문자열로 정의`되어 있음

    ```<python>
        collection_name = "few-shot-examples-collection"                     # <-- 고정된 컬렉션 이름
        vectorstore = Chroma.from_texts(
            ...,
            collection_name=collection_name,
        )
    ```

### 3) 해결 코드:
- `uuid 라이브러리`를 사용 → 동적 이름 생성
- 매번 `새로운 collection_name`을 생성합니다.

    ```<python>
        import uuid

        # ...

        collection_name = f"few-shot-examples-collection-{uuid.uuid4()}"      # <-- 동적으로 변경
        vectorstore = Chroma.from_texts(
            ...,
            collection_name=collection_name,                                  # 수정된 부분
        )
    ``` 

## 3. `TypeError`: `Can't instantiate abstract class` 

### 1) 오류원인: 
- `BaseExampleSelector` 추상 클래스를 상속받았지만, `필수 메서드`인 `add_exampl`e이 `구현되지 않았기 때문`

### 2) 문제 코드:
- `add_example 메서드`가 클래스 내부에 정의되어 있지 않았음

    ```<python>
        class CustomInstructionExampleSelector(BaseExampleSelector):
            def __init__(self, examples: List[Dict], embeddings: Any, k: int = 1):
                ...

            # def_add_example 빠져있음

            def select_examples(self, input_variables: Dict[str, str]) -> List[Dict]:
                ...
    ```

### 3) 해결 코드:

- `add_example` 메서드를 클래스 안에 추가하여 `추상 클래스 규칙`을 `만족`시키기

    ```<python>
        class CustomInstructionExampleSelector(BaseExampleSelector):
            def __init__(self, examples: List[Dict], embeddings: Any, k: int = 1):
                ...

            # [해결 부분] 필수 메서드인 'add_example' 추가
            def add_example(self, example: Dict[str, str]) -> Any:
                raise NotImplementedError(
                    "This custom example selector does not support adding examples."
                )

            def select_examples(self, input_variables: Dict[str, str]) -> List[Dict]:
                ...
    ```
