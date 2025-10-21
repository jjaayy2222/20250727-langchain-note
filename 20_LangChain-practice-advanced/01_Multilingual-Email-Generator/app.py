# 새 버전

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM

def getLLMResponse(form_input, email_sender, email_recipient, language):
    """
    getLLMResponse 함수는 주어진 입력을 사용하여 LLM(대형 언어 모델)으로부터 이메일 응답을 생성합니다.

    매개변수:
    - form_input: 사용자가 입력한 이메일 주제.
    - email_sender: 이메일을 보낸 사람의 이름.
    - email_recipient: 이메일을 받는 사람의 이름.
    - language: 이메일이 생성될 언어 (한국어 또는 영어).

    반환값:
    - LLM이 생성한 이메일 응답 텍스트.
    """

    # 💡 설치된 'llama3.2:3b' 모델을 사용하도록 지정했습니다!
    llm = OllamaLLM(model="llama3.2:3b", temperature=0.7)

    # 이메일 생성 프롬프트
    if language == "한국어":
        template = """ 
        다음 정보를 사용하여 전문적인 이메일을 한국어로 작성해 주세요. 
        \n\n이메일 주제: {email_topic}
        \n보낸 사람: {sender}\n받는 사람: {recipient}
        \n\n이메일 내용:
        """
    else: 
        template = """ 
        Write a professional email in English using the following information.
        \n\nEmail Topic: {email_topic}
        \nSender: {sender}\nRecipient: {recipient}
        \n\nEmail content:
        """

    # 최종 PROMPT 생성
    prompt = PromptTemplate(
        input_variables=["email_topic", "sender", "recipient", "language"],
        template=template,
    )

    # LLM을 사용하여 응답 생성
    response = llm.invoke(prompt.format(email_topic=form_input, sender=email_sender, recipient=email_recipient, language=language))
    print(response)

    return response


st.set_page_config(
    page_title="이메일 생성기 📮",
    page_icon='📮',
    layout='centered',
    initial_sidebar_state='collapsed'
)
st.header("이메일 생성기 📮 ")

# 이메일 작성 언어 선택 
language_choice = st.selectbox('이메일을 작성할 언어를 선택하세요:', ['한국어', 'English'])

form_input = st.text_area('이메일 주제를 입력하세요', height=100)

# 사용자 입력을 받기 위한 UI 열 생성
col1, col2 = st.columns([10, 10])
with col1:
    email_sender = st.text_input('보낸 사람 이름')
with col2:
    email_recipient = st.text_input('받는 사람 이름')

submit = st.button("생성하기")

# '생성하기' 버튼이 클릭되면, 아래 코드를 실행합니다.
if submit:
    if not form_input or not email_sender or not email_recipient:
        st.error("이메일 주제, 보낸 사람, 받는 사람 이름을 모두 입력해야 합니다.")
    else:
        with st.spinner('생성 중입니다...'):
            response = getLLMResponse(form_input, email_sender, email_recipient, language_choice)
            st.write(response)

# 해당 폴더로 이동
# streamlit run app.py