### 사용 모델 
    - `gemini-2.5-flash` -> X (max-token 문제 발생)
    - `gemini-1.5-pro` -> X (호출 딜레이 문제 발생)
    - `gemini-1.5-flash` -> O 

---

### cell output

`(lc_env) ➜  01_2_GEMINI_TEST git:(main) ✗ python test_gemini_prompt.py`

* --- 온라인 재무제표 이미지 분석 시작 ---
* [재무제표 분석 답변 (스트리밍)]:

* --- 청크 1 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
 ) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text='물'
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```

  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 물
* 청크 텍스트: 물
* --- 청크 1 종료 ---

* --- 청크 2 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text='론입니다. 아래 표는 2017년, 2'
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 론입니다. 아래 표는 2017년, 2
* 청크 텍스트: 론입니다. 아래 표는 2017년, 2
* --- 청크 2 종료 ---

* --- 청크 3 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text='018년, 2019년의 매출채권'
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 018년, 2019년의 매출채권
* 청크 텍스트: 018년, 2019년의 매출채권
* --- 청크 3 종료 ---

* --- 청크 4 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text=""" 및 재고자산을 보여줍니다.

| 연도 | 매출채권 (백만원) | 재고자산 (백"""
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트:  및 재고자산을 보여줍니다.

* | 연도 | 매출채권 (백만원) | 재고자산 (백
* 청크 텍스트:  및 재고자산을 보여줍니다.

* | 연도 | 매출채권 (백만원) | 재고자산 (백
* --- 청크 4 종료 ---

* --- 청크 5 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text="""만원) |
|---|---|---|
| 2017 | 3,781,000 | 2,07"""
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 만원) |
* |---|---|---|
* | 2017 | 3,781,000 | 2,07
* 청크 텍스트: 만원) |
* |---|---|---|
* | 2017 | 3,781,000 | 2,07
* --- 청크 5 종료 ---

* --- 청크 6 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text="""4,555 |
| 2018 | 4,004,920 | 2,426,364 |
| 2019 | 3,9"""
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 4,555 |
* | 2018 | 4,004,920 | 2,426,364 |
* | 2019 | 3,9
* 청크 텍스트: 4,555 |
* | 2018 | 4,004,920 | 2,426,364 |
* | 2019 | 3,9
* --- 청크 6 종료 ---

* --- 청크 7 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text="""81,935 | 2,670,294 |


**추가 정보:**

* **매출채권:** 2018년에 최고치를 기록했지만,"""
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트: 81,935 | 2,670,294 |


* **추가 정보:**

  * **매출채권:** 2018년에 최고치를 기록했지만,
  * 청크 텍스트: 81,935 | 2,670,294 |


* **추가 정보:**

  * **매출채권:** 2018년에 최고치를 기록했지만,
* --- 청크 7 종료 ---

* --- 청크 8 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text=""" 2019년에는 약간 감소했습니다. 이는 회사의 판매 및 회수 프로세스에 대한 추가 분석이 필요할 수 있음을 시사합니다.
* **재고자산:** 2017년부터 2019년까지 """
      ),
    ],
    role='model'
  )
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  prompt_token_count=383,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=125
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=383
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: None`
  * 후보 0 - `content.parts` 텍스트:  2019년에는 약간 감소했습니다. 이는 회사의 판매 및 회수 프로세스에 대한 추가 분석이 필요할 수 있음을 시사합니다.
* **재고자산:** 2017년부터 2019년까지 
* 청크 텍스트:  2019년에는 약간 감소했습니다. 이는 회사의 판매 및 회수 프로세스에 대한 추가 분석이 필요할 수 있음을 시사합니다.
* **재고자산:** 2017년부터 2019년까지 
* --- 청크 8 종료 ---

* --- 청크 9 시작 ---
* 청크 객체 타입: `<class 'google.genai.types.GenerateContentResponse'>`
* 청크 객체 내용: ```sdk_http_response=HttpResponse(
  headers=<dict len=11>
) candidates=[Candidate(
  content=Content(
    parts=[
      Part(
        text="""꾸준히 증가하고 있습니다. 이는 회사의 생산량 증가 또는 재고 관리 전략 변경을 나타낼 수 있습니다.
이러한 경향에 대한 더 나은 이해를 위해서는 추가적인 재무 정보와 비즈니스 컨텍스트가 필요합니다."""
      ),
    ],
    role='model'
  ),
  finish_reason=<FinishReason.STOP: 'STOP'>
)] create_time=None response_id=None model_version='gemini-1.5-flash' prompt_feedback=None usage_metadata=GenerateContentResponseUsageMetadata(
  candidates_token_count=320,
  candidates_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=320
    ),
  ],
  prompt_token_count=381,
  prompt_tokens_details=[
    ModalityTokenCount(
      modality=<MediaModality.TEXT: 'TEXT'>,
      token_count=123
    ),
    ModalityTokenCount(
      modality=<MediaModality.IMAGE: 'IMAGE'>,
      token_count=258
    ),
  ],
  total_token_count=701
) automatic_function_calling_history=None parsed=None```
  * 후보 0 - `finish_reason: FinishReason.STOP`
  * 후보 0 - `content.parts` 텍스트: 꾸준히 증가하고 있습니다. 이는 회사의 생산량 증가 또는 재고 관리 전략 변경을 나타낼 수 있습니다.

* 이러한 경향에 대한 더 나은 이해를 위해서는 추가적인 재무 정보와 비즈니스 컨텍스트가 필요합니다.
* 청크 텍스트: 꾸준히 증가하고 있습니다. 이는 회사의 생산량 증가 또는 재고 관리 전략 변경을 나타낼 수 있습니다.

* 이러한 경향에 대한 더 나은 이해를 위해서는 추가적인 재무 정보와 비즈니스 컨텍스트가 필요합니다.
* --- 청크 9 종료 ---

* --- 재무제표 분석 종료 ---

* 모델 사용 완료

---

### 정리
- 물론입니다. 아래 표는 2017년, 2018년, 2019년의 매출채권 및 재고자산을 보여줍니다.

- | 연도 | 매출채권 (백만원) | 재고자산 (백만원) |
- |---|---|---|
- | 2017 | 3,781,000 | 2,074,555 |
- | 2018 | 4,004,920 | 2,426,364 |
- | 2019 | 3,981,935 | 2,670,294 |

- **추가 정보:**

  - **매출채권:** 2018년에 최고치를 기록했지만, 2019년에는 약간 감소했습니다. 이는 회사의 판매 및 회수 프로세스에 대한 추가 분석이 필요할 수 있음을 시사합니다.
  - **재고자산:** 2017년부터 2019년까지 꾸준히 증가하고 있습니다. 이는 회사의 생산량 증가 또는 재고 관리 전략 변경을 나타낼 수 있습니다.

- 이러한 경향에 대한 더 나은 이해를 위해서는 추가적인 재무 정보와 비즈니스 컨텍스트가 필요합니다.
