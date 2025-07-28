import os
import requests # 온라인 이미지 다운로드를 위해 requests 라이브러리 추가
from dotenv import load_dotenv
from google import genai
from PIL import Image # Image.open()을 위해 PIL (Pillow) 라이브러리 필요

# .env 파일 로드 (GEMINI_API_KEY 환경 변수 포함)
load_dotenv()

# 환경 변수에서 GEMINI_API_KEY 가져오기
# genai.Client()는 기본적으로 이 환경 변수를 찾습니다.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

# GenAI 클라이언트 객체 생성
client = genai.Client(api_key=api_key)

# 사용할 Gemini 모델 지정 (Jay님의 요청에 따라 'gemini-2.5-flash-lite' 사용)
# 만약 'gemini-2.5-flash-lite' 모델이 더 이상 제공되지 않거나 문제가 발생할 경우,
# 'gemini-1.5-flash' 또는 'gemini-1.5-pro'와 같은 현재 사용 가능한 최신 모델을 고려해야 할 수 있습니다.
# 현재 시점(2025년 7월)에서 'gemini-2.5-flash-lite'가 유효하다는 전제하에 진행합니다.
MODEL_NAME = 'gemini-2.5-flash'

# --- 이미지 파일 경로 설정 ---
# 이미지 파일은 모두 교재와 똑같이 설정 

# 1. 로컬 이미지 파일 경로
LOCAL_IMAGE_PATH = "../images/sample-image.png"

# 2. 온라인 이미지 URL 
ONLINE_IMAGE_URL = "https://t3.ftcdn.net/jpg/03/77/33/96/360_F_377339633_Rtv9I77sSmSNcev8bEcnVxTHrXB4nRJ5.jpg"

# --- 이미지 로드 함수 ---
def load_image_from_path(image_path):
    """로컬 파일 경로에서 이미지를 로드합니다."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"오류: 로컬 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다. 경로를 확인해주세요.")
    return Image.open(image_path)

def load_image_from_url(image_url):
    """온라인 URL에서 이미지를 다운로드하여 로드합니다."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status() # HTTP 오류가 발생하면 예외 발생
        return Image.open(response.raw)
    except Exception as e:
        raise ConnectionError(f"오류: 온라인 이미지 '{image_url}'을(를) 로드하는 데 실패했습니다: {e}")

try:
    # --- 로컬 이미지로 멀티모달 스트리밍 ---
    print("\n--- 로컬 이미지로 멀티모달 스트리밍 시작 ---")
    local_image = load_image_from_path(LOCAL_IMAGE_PATH)

    # 모델에 로컬 이미지와 텍스트 프롬프트 전달 (스트리밍)
    local_image_response_chunks = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=[
            local_image,
            '이 로컬 이미지에 대해 자세히 설명하고, 스트리밍 형식으로 답변해 주세요.'
        ]
    )

    print("[로컬 이미지 답변 (스트리밍)]:")
    for chunk in local_image_response_chunks:
        print(chunk.text, end='') # 스트리밍이므로 한 조각씩 출력
    print("\n--- 로컬 이미지 스트리밍 종료 ---\n")

    # --- 온라인 이미지로 멀티모달 스트리밍 ---
    print("\n--- 온라인 이미지로 멀티모달 스트리밍 시작 ---")
    online_image = load_image_from_url(ONLINE_IMAGE_URL)

    # 모델에 온라인 이미지와 텍스트 프롬프트 전달 (스트리밍)
    online_image_response_chunks = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=[
            online_image,
            '이 온라인 이미지에 대해 자세히 설명하고, 스트리밍 형식으로 답변해 주세요.'
        ]
    )

    print("[온라인 이미지 답변 (스트리밍)]:")
    for chunk in online_image_response_chunks:
        print(chunk.text, end='') # 스트리밍이므로 한 조각씩 출력
    print("\n--- 온라인 이미지 스트리밍 종료 ---\n")

except FileNotFoundError as e:
    print(f"파일 오류: {e}")
except ConnectionError as e:
    print(f"네트워크 오류: {e}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")

print("모델 사용 완료")
