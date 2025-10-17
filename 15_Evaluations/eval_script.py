# eval_script.py

from dotenv import load_dotenv
load_dotenv()

import os
from myrag4 import PDFRAG
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith.evaluation import evaluate, LangChainStringEvaluator

print("🚀 RAG 시스템 초기화 시작...\n")

# 현재 스크립트 위치 확인
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📂 스크립트 위치: {script_dir}\n")

# PDF 파일 절대 경로 생성
pdf_path = os.path.join(script_dir, "data", "SPRI_AI_Brief_2023년12월호_F.pdf")
print(f"📄 PDF 경로: {pdf_path}")

# 파일 존재 확인
if not os.path.exists(pdf_path):
    print(f"❌ 파일이 존재하지 않습니다!")
    print(f"❌ 경로: {pdf_path}\n")
    
    # data 폴더 내용 확인
    data_dir = os.path.join(script_dir, "data")
    if os.path.exists(data_dir):
        print(f"📁 data 폴더 내용:")
        for file in os.listdir(data_dir):
            print(f"   - {file}")
    else:
        print(f"❌ data 폴더가 존재하지 않습니다!")
    
    exit(1)

print(f"✅ 파일 확인 완료!\n")

# LLM 생성
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)
print("✅ LLM 생성 완료: gemini-2.5-flash-lite\n")

# RAG 생성
rag = PDFRAG(
    pdf_path,  # 절대 경로 사용!
    llm,
    chunk_size=300,
    chunk_overlap=50,
)

# Retriever & Chain (k=7!)
retriever = rag.create_retriever(k=7)
chain = rag.create_chain(retriever)

print("\n" + "="*50)
print("🧪 테스트 실행...")
print("="*50 + "\n")

# 테스트
test_question = "삼성전자가 자체 개발한 생성형 AI의 이름은 무엇인가요?"
test_answer = chain.invoke(test_question)
print(f"질문: {test_question}")
print(f"답변: {test_answer}\n")

print("="*50)
print("📊 평가 시작...")
print("="*50 + "\n")

# 질문 함수
def ask_question(inputs: dict):
    return {"answer": chain.invoke(inputs["question"])}

# 평가자 생성
qa_evaluator = LangChainStringEvaluator(
    "qa",
    config={"llm": llm}
)


# 평가 실행
try:
    experiment_results = evaluate(
        ask_question,
        data="RAG_EVAL_DATASET",
        evaluators=[qa_evaluator],
        experiment_prefix="RAG_EVAL_K7",
        metadata={
            "variant": "k=7, chunk_size=300",
        },
        max_concurrency=1,
    )
    
    print("\n" + "="*50)
    print("✅ 평가 완료!")
    print("="*50)
    print(f"\n결과: {experiment_results}\n")
    
except Exception as e:
    print(f"\n❌ 에러 발생: {e}\n")
