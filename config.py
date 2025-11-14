# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# langchain-note/config.py 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""" OpenAI 모델 설정 함수
- gpt-5-nano / gpt-5-mini
- text-embedding-3-small / text-embedding-3-large
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 환경변수 로드
load_dotenv()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━
# 전역 변수: LLM 설정 (프록시 기반)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━

# GPT-5-nano 기본 설정 (프록시 경유)
gpt_5_nano = ChatOpenAI(
    api_key=os.getenv("GPT5_NANO_API_KEY"),
    base_url=os.getenv("GPT5_NANO_BASE_URL"),
    model=os.getenv("GPT5_NANO_MODEL", "openai/gpt-5-nano"),
    #temperature=0.7
)

# GPT-5-mini 설정 (프록시 경유)
gpt_5_mini = ChatOpenAI(
    api_key=os.getenv("GPT5_MINI_API_KEY"),
    base_url=os.getenv("GPT5_MINI_BASE_URL"),
    model=os.getenv("GPT5_MINI_MODEL", "openai/gpt-5-mini"),
    #temperature=0.7
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━
# 전역 변수: Embeddings 설정 (프록시 기반)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("EMBEDDING_API_KEY"),
    base_url=os.getenv("EMBEDDING_BASE_URL"),
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
)

# text-embedding-3-large 설정 (프록시 경유)
embeddings_large = OpenAIEmbeddings(
    api_key=os.getenv("EMBEDDING_LARGE_API_KEY"),
    base_url=os.getenv("EMBEDDING_LARGE_BASE_URL"),
    model=os.getenv("EMBEDDING_LARGE_MODEL", "text-embedding-3-large")
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━
# 도우미 함수: 동적 모델 변경
# ━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_llm(model=(os.getenv("GPT5_MINI_MODEL", "openai/gpt-5-mini"))):
    """
    동적 LLM 생성 함수 (프록시 기반)
    
    Args:
        model_name: 사용할 모델 이름 (gpt_5_nano 또는 gpt_5_mini)
    
    Returns:
        설정된 LLM 객체
    """
    if model== os.getenv("GPT5_MINI_MODEL", "openai/gpt-5-mini"):
        return gpt_5_nano
    return gpt_5_mini


def get_embeddings(model=(os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))):
    """
    동적 Embeddings 생성 함수
    
    Args:
        model_name: 사용할 임베딩 모델 이름
    
    Returns:
        설정된 Embeddings 객체
    """
    if model== os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"):              # text-embedding-3-small (기본)
        return embeddings
    return embeddings_large

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 메인 실행 (테스트용 / 함수 호출 기반으로 변경)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("🔍 LangChain Note Config 테스트 (프록시 기반)")
    print("=" * 50)
    
    # 질의내용
    question = "대한민국의 수도는 어디인가요?"
    
    # 1. 직접 호출 테스트
    print("\n1️⃣ 직접 호출 (gpt_5_nano):", "\n")
    response1 = gpt_5_nano.invoke(question)
    print(f"   답변: {response1.content}")
    print("-" * 50, "\n")

    # 2. 함수 호출 테스트 (기본값)
    print("\n2️⃣ 함수 호출 get_llm() [기본값]:", "\n")
    llm = get_llm()
    response2 = llm.invoke(question)
    print(f"   답변: {response2.content}")
    print("-" * 50, "\n")

    # 3. 함수 호출 테스트 (gpt-5-mini) - 명시적 호출
    print("\n3️⃣ 함수 호출 get_llm() [gpt-5-mini]:", "\n")
    llm = get_llm("openai/gpt-5-mini")
    response3 = llm.invoke(question)
    print(f"   답변: {response3.content}")
    print("-" * 50, "\n")

    # 4. 임베딩 테스트
    text = "임베딩 테스트 문장"

    print("\n4️⃣ Embeddings 테스트:")
    emb_small = get_embeddings("small")
    vec_small = emb_small.embed_query(text)
    print(f"   small: {len(vec_small)}차원")
    
    emb_large = get_embeddings("large")
    vec_large = emb_large.embed_query(text)
    print(f"   large: {len(vec_large)}차원")
    
    print("\n" + "=" * 50)
    print("✅ 모든 테스트 완료!")

    
    
"""test_result → ⭕️ (but, 개별 함수로 호출함)

    python -m config
    
    🔍 LangChain Note Config 테스트 (프록시 기반)
    ==================================================

    1️⃣ 기본 LLM (gpt-5-nano): 

    [전체 답변]: content='대한민국의 수도는 서울특별시(서울)입니다. 필요하신 정보가 더 있나요?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 224, 'prompt_tokens': 15, 'total_tokens': 239, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 192, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-CbgLVwFqErslOfV9Kl12BW4dqpwAm', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--90484fd4-62e1-4d4b-9b66-63beb12437d8-0' usage_metadata={'input_tokens': 15, 'output_tokens': 224, 'total_tokens': 239, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 192}}
    --------------------------------------------------
    [답변]:대한민국의 수도는 서울특별시(서울)입니다. 필요하신 정보가 더 있나요?
    --------------------------------------------------
    [메타데이터]]: {'input_tokens': 15, 'output_tokens': 224, 'total_tokens': 239, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 192}}
    --------------------------------------------------

    2️⃣ 변경된 LLM (gpt-5-mini): 

    [전체 답변]: content='대한민국의 수도는 서울특별시입니다. 다만 일부 중앙행정기관과 행정 기능은 세종특별자치시로 이전되어 행정 중심 기능이 분산되어 있습니다.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 308, 'prompt_tokens': 15, 'total_tokens': 323, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-mini-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-CbgLYTNhe6D7LNYETiGdOt2lHFh9U', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--29108493-8737-4d56-9959-1ead94f684f2-0' usage_metadata={'input_tokens': 15, 'output_tokens': 308, 'total_tokens': 323, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}}
    -------------------------------------------------- 

    [답변]:대한민국의 수도는 서울특별시(서울)입니다. 필요하신 정보가 더 있나요?
    -------------------------------------------------- 

    [메타데이터]]: {'input_tokens': 15, 'output_tokens': 224, 'total_tokens': 239, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 192}}
    -------------------------------------------------- 


    3️⃣ 기본 Embeddings (text-embedding-3-small): 

    [-0.00776276458054781, 0.03680367395281792, 0.019545823335647583, -0.0196656696498394, 0.017203375697135925]

    ==================================================

        차원: 1536차원

    4️⃣ 변경된 Embeddings (text-embedding-3-large): 

    [-0.00311934482306242, -0.007872357964515686, -0.012800268828868866, 0.030090242624282837, 0.016375118866562843]

    ==================================================

        차원: 3072차원

    ============================

"""


"""test_result_2 → ⭕️ (함수로 호출)


    python -m config

    🔍 LangChain Note Config 테스트 (프록시 기반)
    ==================================================

    1️⃣ 직접 호출 (gpt_5_nano): 

    답변: 대한민국의 수도는 서울(서울특별시)입니다.
    -------------------------------------------------- 


    2️⃣ 함수 호출 get_llm() [기본값]: 

    답변: 대한민국의 수도는 서울(서울특별시)입니다.
    -------------------------------------------------- 


    3️⃣ 함수 호출 get_llm() [gpt-5-mini]: 

    답변: 서울특별시입니다.
    -------------------------------------------------- 


    4️⃣ Embeddings 테스트:
    small: 3072차원
    large: 3072차원

    ==================================================
    ✅ 모든 테스트 완료!

"""



