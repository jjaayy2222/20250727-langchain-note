import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image               # 이미지 처리를 위해 필요
import requests                     # URL에서 이미지를 가져오기 위해 필요
from io import BytesIO              # requests.get(stream=True)와 Image.open을 연결하기 위해 필요

# .env 파일 로드 (GEMINI_API_KEY 환경 변수 포함)
load_dotenv()

# 환경 변수에서 GEMINI_API_KEY 가져오기
# genai.Client()는 기본적으로 이 환경 변수를 찾습니다.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

# --- 1. Gemini API 클라이언트 생성 ---
client = genai.Client(api_key=api_key)

# 사용할 모델
MODEL_NAME = 'gemini-1.5-flash' 

# --- 2. 이미지 로드 헬퍼 함수 정의 ---
def load_image_from_url(image_url):
    """온라인 URL에서 이미지를 다운로드하여 PIL.Image 객체로 로드합니다."""
    try:
        response = requests.get(image_url)
        response.raise_for_status() # HTTP 오류가 발생하면 예외 발생
        return Image.open(BytesIO(response.content)) # BytesIO를 사용하여 이미지 로드
    except Exception as e:
        raise ConnectionError(f"오류: 온라인 이미지 '{image_url}'을(를) 로드하는 데 실패했습니다: {e}")
    
# 사용자에게 보여줄 질문 (모델의 실제 입력 내용)
# user_prompt = """당신에게 주어진 표는 회사의 재무제표 입니다. 흥미로운 사실을 정리하여 답변하세요."""  -> 구체적이고 명확하게 질문하기
user_prompt =  """이 재무제표 이미지에서 2019년, 2018년, 2017년의 매출채권과 재고자산 값을 각각 알려주세요. 표 형식으로 정리해 주세요.""" 

# 분석할 재무제표 이미지 URL
ONLINE_IMAGE_URL = "https://storage.googleapis.com/static.fastcampus.co.kr/prod/uploads/202212/080345-661/kwon-01.png"

# --- 4. GenerateContentConfig 설정 ---
# 모델의 역할 (System Instruction)과 응답 생성 파라미터들을 config 객체 안에 정의합니다.
generation_config = types.GenerateContentConfig(
    system_instruction="""당신은 표(재무제표) 를 해석하는 금융 AI 어시스턴트 입니다. 
당신의 임무는 주어진 테이블 형식의 재무제표를 바탕으로 흥미로운 사실을 정리하여 친절하게 답변하는 것입니다.""",
    max_output_tokens=4096,     # 최대 출력 토큰 수 (재무제표 설명은 길 수 있으므로 충분히 확보) / 800 -> 2000 -> 4096 (응답 길이 확장)ß
    top_k=40,                   # 샘플링 시 상위 K개의 토큰만 고려 (다양성 제어) / 5 -> 40 (다양성 증가)
    top_p=0.9,                  # 누적 확률 P 이내의 토큰만 고려 (다양성 제어) / 0.8 -> 0.9 (다양성 증가)
    temperature=0.9,            # 응답의 창의성/무작위성 조절 (높을수록 창의적) / 0.8 -> 0.9 (창의성 증가)
    seed=42,                    # 재현 가능한 결과를 위한 시드값
    # response_mime_type='application/json', # JSON 응답이 필요하지 않으므로 주석 처리
    # stop_sequences=['\n'], # 스트리밍 시 답변이 중간에 끊길 수 있으므로 주석 처리
)

# --- 5. 모델 호출 (멀티모달 스트리밍) ---
print("\n--- 온라인 재무제표 이미지 분석 시작 ---")

try:
    # 재무제표 이미지 로드
    financial_statement_image = load_image_from_url(ONLINE_IMAGE_URL)

    # models.generate_content_stream 호출
    # contents: 이미지와 유저 프롬프트 (모델의 실제 입력)
    # config: 모델의 행동 방식과 생성 파라미터 (system_instruction 포함)
    response_chunks = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=[
            financial_statement_image,
            {'text': user_prompt} 
        ],
        config=generation_config,               # config 인자로 GenerateContentConfig 객체 전달
    )

    print("[재무제표 분석 답변 (스트리밍)]:")
    # --- 디버깅 코드 추가 ---
    all_response_text = ""
    for i, chunk in enumerate(response_chunks):
        print(f"\n--- 청크 {i+1} 시작 ---")
        print(f"청크 객체 타입: {type(chunk)}")
        print(f"청크 객체 내용: {chunk}") # 전체 청크 객체 출력

        if hasattr(chunk, 'candidates') and chunk.candidates:
            for cand_idx, candidate in enumerate(chunk.candidates):
                print(f"  후보 {cand_idx} - finish_reason: {candidate.finish_reason}")
                if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                    print(f"  후보 {cand_idx} - safety_ratings: {candidate.safety_ratings}")
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        # content.parts에서 텍스트 부분만 추출
                        part_texts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        print(f"  후보 {cand_idx} - content.parts 텍스트: {''.join(part_texts)}")
        
        # 실제 출력될 텍스트 부분
        if chunk.text:
            print(f"청크 텍스트: {chunk.text}")
            all_response_text += chunk.text
        else:
            print("청크에 텍스트 없음 (chunk.text is None or empty)")
        print(f"--- 청크 {i+1} 종료 ---")
    # --- 디버깅 코드 끝 ---
    
    # 최종 응답이 None이 아닌지 확인
    if not all_response_text.strip(): # 공백만 있는 경우도 None으로 간주
        print("\n[경고: 모델이 텍스트를 생성하지 않았습니다. 위 디버깅 로그를 확인하세요.]")

    print("\n--- 재무제표 분석 종료 ---\n")

except ConnectionError as e:
    print(f"네트워크 오류: {e}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")

print("모델 사용 완료")
