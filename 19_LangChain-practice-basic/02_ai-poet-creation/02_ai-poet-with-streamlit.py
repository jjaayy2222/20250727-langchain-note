# 환경변수 처리 및 클라이언트 생성
from langsmith import Client
from dotenv import load_dotenv

import os
import json

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

#제목
st.title("인공지능 시인")

# content 미리 설정해보기 = "코딩"
content = "코딩"
result = chain.invoke({"input": content + "에 대한 시를 써줘"})
print(result)

# 출력해보기
st.title("This is a title")
st.title("_Streamlit_is :blue[cool] :sunglasses:")
