#################################        
# 필요한 모듈 임포트
#################################     
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import streamlit as st                          # 스트림릿 사용에 필요한 모듈 임포트

# gpt, gemini 스위치되도록 테스트
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
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

#################################   
# 문자열 출력 파서
#################################   
output_parser = StrOutputParser()

#################################   
#LLM 체인 구성
#################################   
chain = prompt | llm | output_parser


#################################   
# Streamlit 
#################################   

# 1. 제목
st.title("인공지능 시인")

# 2. 시 주제 입력 필드
# st.text_input(입력 필드의 목적을 설명하는 label) = 입력값 → content에 저장
content = st.text_input("시의 주제를 제시해주세요")

# st.write() = 화면에 텍스트를 표시하는 함수
# "시의 주제는" +(더하기 연산자) content 변수값
st.write("시의 주제는", content)


# 3. 실행 버튼 설정하기 
# 시 작성 요청하기 = st.button() = if문을 통해 사용자가 버튼을 눌렀을 때 실행할 동작 명시
# st.button() → → chain.invoke() = ({"input": content + "에 대한 시를 써줘"})

if st.button("시 작성 요청하기"):
    with st.spinner('Wait for it...'):                  # 로딩 애니메이션 설정 (with 키워드 아래에 있는 코드 블럭에만 적용)
        result = chain.invoke({"input": content + "에 대한 시를 써줘"})
        st.write(result)