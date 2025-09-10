# 🚀 Streamlit 앱 배포 - Gemini API 타임아웃 해결

>> **작성일:** 2025-09-10
>>  
>> **작성자:** Jay  
>> 
>> **배포 앱:** [AI 시인](https://ai-poet-with-gemini-flash-lite.streamlit.app/)

---

## 1. 문제 상황

- **현상:**  
  - `Streamlit Community Cloud`배포 후 **`504 Deadline Exceeded` 에러** 지속 발생
  - `langchain_google_genai.chat_models._chat_with_retry` 재시도 반복
  - 로컬에서는 정상 작동하지만 **클라우드에서 타임아웃**

- **에러 로그:**

  ```python
    Retrying langchain_google_genai.chat_models._chat_with_retry.<locals>._chat_with_retry 
    in 2.0 seconds as it raised DeadlineExceeded: 504 Deadline Exceeded.
  ```

<br>

## 2. 원인 분석

1. **`환경변수 누락`**
   - `.env` 파일이 `.gitignore`에 포함되어 배포 시 제외
   - `Streamlit Community Cloud`에서 `GOOGLE_API_KEY` 접근 불가

2. **네트워크 지연**
   - 클라우드 환경에서 `Gemini API 응답 지연`
   - 기본 타임아웃 설정 부족

<br>

## 3. 해결 방법

### 3.1 환경변수 직접 설정 (핵심 해결책)
- `Streamlit Community Cloud` **`Settings`** **→ `Secrets`**에서 직접 설정:
  
  ```python

    # NOLM 형식으로 작성해야함
    
    OPENAI_API_KEY = "sk-..."
    
    GOOGLE_API_KEY = "AIza..."
  
  ```

- 앱 재배포 후 **`즉시 해결 확인`**
  
  ![시 생성 성공](../../19_LangChain-practice-basic/02_ai-poet-creation/img/04_depolyment_5.png)

<br>

### 3.2 추가 최적화 방안
- **`타임아웃 설정 증가 고려`**
- **`OpenAI 백업` 모델 설정 검토**
- **`에러 핸들링 및 재시도 로직 강화`**

<br>

## 4. 결과 검증

✅ **배포 성공**: [**`인공지능 시인`**](https://ai-poet-with-gemini-flash-lite.streamlit.app/)

✅ **시 생성 완료**

  ```markdown

  ## 당신의 하루, 작은 별 하나

  창가에 내려앉은 햇살은 먼지 쌓인 책갈피처럼 따스한 온기를 품고 있네요. 오늘도 당신의 하루는 어김없이 흘러가고 있겠지요.

  어쩌면 잊고 있었을지도 모를 작은 화분의 푸른 잎사귀, 밤새도록 별을 헤며 가만히 숨죽여 피어났을 수줍은 꽃봉오리처럼.

  거친 손끝에 묻은 흙먼지는 당신의 성실함의 흔적이자 세상에 작은 씨앗을 심는 고귀한 노동의 증표일 거예요.

  익숙한 길모퉁이, 어느새 붉게 물든 단풍잎 하나 바람에 흩날리며 속삭이듯 고요한 당신의 마음에도 작은 떨림이 깃들었기를.

  오늘, 당신이 건넨 말 한마디가 누군가의 마음에 작은 별 하나를 심어주었다면, 그것으로 충분한 하루가 될 수 있겠죠.

  저무는 해를 바라보며 오늘 하루의 소란함이 잔잔한 호수에 물결처럼 스르르 가라앉기를.

  내일 아침, 새로운 햇살과 함께 다시 시작될 당신의 하루에 작은 기쁨과 평안이 별빛처럼 내려앉기를.

  ```


✅ **UI/UX 완성**: 반응형 디자인, 호버 효과 정상 작동  

✅ **성능 안정화**: 초기 로딩 후 빠른 응답 속도  

<br>

## 5. 교훈

- **환경변수 관리**: 배포 환경별 `설정 사전 확인 필수`
- **API 의존성**: 클라우드 환경에서의 `외부 API 호출 제약 고려`
- **문서화 중요성**: `트러블슈팅 과정 상세 기록`으로 학습 효과 극대화
- **성취감**: 어려움 극복 후 얻는 성공의 가치

<br>

## 6. 향후 개선
- `환경변수 체크리스트` 작성
- `다중 API 백업 전략` 수립  
- `배포 자동화 스크립트 개발` 검토