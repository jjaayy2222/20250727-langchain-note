import streamlit as st                          # 스트림릿 사용에 필요한 모듈 임포트
import time

# 필요한 모듈 임포트
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import os
import json
from dotenv import load_dotenv

load_dotenv()

# 환경변수에서 API 키 가져오기
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

#################################   
# LLM 설정
#################################   
def get_llm(provider: str):
    """provider에 따라 LLM 객체 반환"""
    if provider == "openai":
        return init_chat_model(
            model="gpt-4o-mini",                    # 사용하는 gpt 모델
            model_provider="openai",
            temperature=0.7,
            api_key=openai_key,
            max_output_tokens=1024
        )
    elif provider == "google":
        return init_chat_model(
            model="gemini-2.5-flash-lite",          # 사용하는 gemini 모델
            model_provider="google_genai",
            temperature=0.7,
            api_key=google_key,
            max_output_tokens=4096
        )
    else:
        raise ValueError("지원하지 않는 provider입니다.")

# 🔄 원하는 모델 선택
llm = get_llm("google")                             # "openai"로 바꾸면 gpt 사용 가능 

#################################   
# 프롬프트 템플릿 생성
#################################   
#프롬프트 템플릿 생성
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{topic}에 대한 {style} 스타일의 시를 {poet} 시인의 문체를 참고해서 시를 써줘.")
])

#################################   
# 문자열 출력 파서
#################################   
output_parser = StrOutputParser()

#################################   
#LLM 체인 구성
#################################   
chain = prompt2 | llm | output_parser

#################################   
# Streamlit 
#################################   

# 1. 제목 및 소개
# HTML/CSS를 사용하여 제목과 이모지를 가운데로 정렬해보기
st.markdown(
    """
    <div style="text-align: center;">
        <h1><span style='font-size: 2.5rem;'>🤖</span> 인공지능 시인 <span style='font-size: 2.5rem;'>✒️</span></h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)                         # 줄바꿈 추가

# 2. 입력 필드 (주제, 스타일, 참고 시인)
# st.write() = 화면에 텍스트를 표시하는 함수
topic = st.text_input(" • 시의 주제를 입력하세요 : ")
st.write("시의 주제는 ", topic)
st.markdown("<br>", unsafe_allow_html=True)                         # 줄바꿈 추가

style = st.text_input(" • 시의 스타일을 입력하세요 (예: 감성적인, 유머러스한) : ")
st.write("시의 스타일은 ", style)
st.markdown("<br>", unsafe_allow_html=True)                         # 줄바꿈 추가

poet = st.text_input(" • 참고할 시인의 이름을 입력하세요 (예: 김소월, 윤동주) : ")
st.write("참고할 시인은 ", poet)
st.markdown("<br>", unsafe_allow_html=True)                         # 줄바꿈 추가


# 3. 실행 버튼 설정하기

# st.markdown 함수를 사용하여 버튼 컨테이너에 CSS 스타일 적용
# st.columns를 사용하여 버튼을 가운데로 정렬합니다.
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #d3d3d3;      /* 호버 효과 색상을 더 진하게 변경 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(" ✒️__시 작성 요청하기__✒️ "):
        # 입력 필드가 비어있으면 경고 메시지 표시
        if not topic or not style or not poet:
            st.warning(" ⚠️ 모든 항목을 입력해 주세요! ⚠️ ")
        else:
            # 로딩 애니메이션 설정 (with 키워드 아래에 있는 코드 블록에만 적용)
            with st.spinner('⏳ ... Wait for it ... ⏳'):
                # 체인 실행
                result = chain.invoke({
                    "topic": topic,
                    "style": style,
                    "poet": poet
                    })
                time.sleep(5)                                               # 5초 동안 대기
                st.write(result)