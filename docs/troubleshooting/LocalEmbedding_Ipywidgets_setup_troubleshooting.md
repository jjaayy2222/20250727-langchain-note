# 🛠 ipywidgets 설치 및 로컬 임베딩 모델 교체 Troubleshooting

> **작성일:** 2025-09-05  
>
> **작성자:** Jay 

---

## 1. 문제 상황

- **현상 1:**  
  - `Jupyter Notebook 환경`에서 `ipywidgets` 관련 기능이 동작하지 않음.  
    - 예: 대화형 위젯 출력이 표시되지 않거나, `ModuleNotFoundError: No module named 'ipywidgets'` 발생.

- **현상 2:**  
  - 기존 OpenAI 임베딩 모델(`text-embedding-3-small`) 사용 시 `API 호출 의존성`으로 인해 **`로컬 환경`에서 오프라인 `실행 불가`**.

<br>

## 2. 원인 분석

1. **ipywidgets 미설치**
   - 일부 Python 환경(특히 가상환경)에서는 `ipywidgets`가 기본 포함되지 않음.
   - Notebook에서 위젯 렌더링 시 필수 패키지.

2. **임베딩 모델 의존성**
   - OpenAI 임베딩 모델은 API 키와 인터넷 연결이 필요.
   - 오프라인 환경 또는 API 호출 제한 시 사용 불가.

<br>

## 3. 해결 방법

### 3.1 ipywidgets 설치
  - 설치 후 Jupyter Notebook 재시작.

    ```bash
        pip install ipywidgets
    ```

   - 정상적으로 대화형 위젯 출력 확인.

<br>

### 3.2 로컬 임베딩 모델로 교체

- 모델: **`sentence-transformers/all-MiniLM-L6-v2`**

- 장점:
  - `API 키 불필요`
  - 오프라인 환경에서도 동작
  - 빠른 임베딩 생성 속도

- 코드 변경 포인트:
  - `OpenAIEmbeddings` **→ `SentenceTransformer`로 교체**
  - `embedding_function=embed_model.encode` 적용
  - 차원 수는 `embed_model.get_sentence_embedding_dimension()`로 자동 계산

<br>

## 4. 교훈

- `환경별 필수 패키지`(`ipywidgets` 등)는 `사전`에 `설치 여부 확인 필요`.
- `API 기반 모델`은 `편리`하지만, `오프라인 환경 대비책`으로 `로컬 모델 준비`가 `안정적`.
- 벡터스토어 초기화 시 임베딩 차원 수를 코드에서 자동 계산하면 모델 교체가 용이.

<br>

## 5. 향후 개선 아이디어

- 프로젝트 초기화 스크립트에 필수 패키지 설치 절차 포함.
- 로컬/클라우드 환경에 따라 임베딩 모델을 자동 선택하는 설정 추가.
- 환경 세팅 및 `Troubleshooting` 문서를 프로젝트 저장소에 포함.