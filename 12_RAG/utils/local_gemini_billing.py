# 제미나이 모델의 토큰 사용량을 Google GenAI SDK를 사용하여 직접 확인하는 코드

# 필요한 라이브러리 import
import os
from dotenv import load_dotenv
from google import genai                                # Google GenAI SDK import
from google.genai.errors import APIError

# .env 파일에서 환경 변수 로드
load_dotenv()

# GOOGLE_API_KEY 확인 (로컬 환경 변수 사용)
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해 주세요.")

# ----------------------------------------------------------------------
# 단계 1: 네이티브 Gemini 클라이언트 초기화
# ----------------------------------------------------------------------
try:
    # 환경 변수에 있는 API 키를 사용하여 클라이언트를 초기화
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
except Exception as e:
    print(f"⚠️ Google GenAI 클라이언트 초기화 오류: {e}")
    exit()

# ----------------------------------------------------------------------
# 단계 2: 모델 호출 (generate_content 사용)
# ----------------------------------------------------------------------

# 사용자 쿼리
model_name = "gemini-2.5-flash-lite"
query = "대한민국의 수도는 어디인가요?"

print(f"사용 모델: {model_name}")
print(f"질문: {query}\n")

try:
    # 네이티브 SDK의 generate_content 메서드를 호출
    # 이 메서드는 토큰 사용량 정보가 담긴 'usage_metadata'를 항상 포함하는 응답 객체를 반환
    response = client.models.generate_content(
        model=model_name,
        contents=query,
    )
    
    # ----------------------------------------------------------------------
    # 단계 3: 응답 및 토큰 사용량 추출
    # ----------------------------------------------------------------------

    # 응답 내용 출력
    print(f"응답: {response.text}")
    
    # 응답 객체에서 usage_metadata를 직접 추출합니다.
    usage = response.usage_metadata
    
    print("\n--------------------------------------------------")
    print("✨ Gemini 모델 API 토큰 사용량 (과금 정보) ✨")
    # 네이티브 SDK 응답 객체에서 토큰 정보를 가져옵니다.
    print(f"  - 입력(프롬프트) 토큰: {usage.prompt_token_count}")
    print(f"  - 출력(응답) 토큰: {usage.candidates_token_count}")
    print(f"  - 전체 사용 토큰: {usage.total_token_count}")
    print("--------------------------------------------------")

except APIError as e:
    print(f"\n❌ Gemini API 호출 오류가 발생했습니다: {e}")
    print("   -> API 키가 유효한지, 또는 과금 설정에 문제가 없는지 확인해 주세요.")
except Exception as e:
    print(f"\n❌ 예측하지 못한 오류: {e}")