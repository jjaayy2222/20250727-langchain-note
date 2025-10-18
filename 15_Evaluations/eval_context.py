# eval_script.py

from dotenv import load_dotenv
load_dotenv()

import os
from myrag5 import PDFRAG
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith.evaluation import evaluate, LangChainStringEvaluator

print("🚀 Context 기반 평가 시작...\n")

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
    exit(1)
    
print(f"✅ PDF 확인: {pdf_path}\n")
    

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

# Retriever & Chain (k 늘리기)
retriever = rag.create_retriever(k=10)

# Context 포함 체인 생성
chain_with_context = rag.create_chain_with_context(retriever)

print("\n" + "="*50)
print("🧪 테스트 실행...")
print("="*50 + "\n")

# 테스트
test_question = "삼성전자가 자체 개발한 생성형 AI의 이름은 무엇인가요?"
test_result = chain_with_context.invoke(test_question)
print(f"질문: {test_question}")
print(f"Context: {test_result['context'][:200]}...")
print(f"답변: {test_result['answer']}\n")

# ========================================
# Context 기반 평가 함수
# ========================================

def context_answer_rag_answer(inputs: dict):
    """
    Context와 Answer를 함께 반환
    
    Returns
    -------
    dict
        - context: 검색된 Context
        - answer: LLM 답변
        - query: 질문
    """
    result = chain_with_context.invoke(inputs["question"])
    return {
        "context": result["context"],
        "answer": result["answer"],
        "query": inputs["question"],
    }

# ========================================
# 평가자 생성
# ========================================

print("="*50)
print("📊 평가자 생성...")
print("="*50 + "\n")

# 1. COT_QA Evaluator (Chain-of-Thought)
cot_qa_evaluator = LangChainStringEvaluator(
    "cot_qa",
    config={"llm": llm},
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],      # LLM 답변
        "reference": run.outputs["context"],      # Context
        "input": example.inputs["question"],      # 질문
    },
)

# 2. Context_QA Evaluator
context_qa_evaluator = LangChainStringEvaluator(
    "context_qa",
    config={"llm": llm},
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],      # LLM 답변
        "reference": run.outputs["context"],      # Context
        "input": example.inputs["question"],      # 질문
    },
)

print("✅ 평가자 생성 완료\n")

# ========================================
# 평가 실행
# ========================================

print("="*50)
print("📊 평가 실행...")
print("="*50 + "\n")

try:
    experiment_results = evaluate(
        context_answer_rag_answer,
        data="RAG_EVAL_DATASET",
        evaluators=[cot_qa_evaluator, context_qa_evaluator],
        experiment_prefix="RAG_EVAL_CONTEXT",
        metadata={
            "variant": "Context 기반 평가 (COT_QA + Context_QA)",
            "k": 7,
            "chunk_size": 300,
        },
        max_concurrency=1,
    )
    
    print("\n" + "="*50)
    print("✅ 평가 완료!")
    print("="*50)
    print(f"\n결과: {experiment_results}\n")
    
except Exception as e:
    print(f"\n❌ 에러 발생: {e}\n")
