# ========================================
# eval_labeled_criteria.py
# 정답 기반 Criteria 평가
# ========================================

from dotenv import load_dotenv
load_dotenv()

import os
from myrag5 import PDFRAG
from langchain_ollama import ChatOllama             # Ollama 사용
from langsmith.evaluation import evaluate, LangChainStringEvaluator
import warnings
warnings.filterwarnings("ignore")

print("🚀 Labeled Criteria 평가 시작...\n")


# ========================================
# 파일 경로 & LLM 설정
# ========================================

script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "data", "SPRI_AI_Brief_2023년12월호_F.pdf")

if not os.path.exists(pdf_path):
    print(f"❌ 파일 없음: {pdf_path}")
    exit(1)

print(f"✅ PDF 확인: {pdf_path}\n")

# LLM 생성

llm = ChatOllama(
    model="qwen2.5-coder:7b-instruct",
    temperature=0
)

print("✅ 로컬 LLM 생성 완료: Qwen2.5-Coder-7B \n")

# ========================================
# RAG 시스템 생성
# ========================================

rag = PDFRAG(pdf_path, llm, chunk_size=300, chunk_overlap=50)
retriever = rag.create_retriever(k=10, search_type="similarity")

# Context 포함 체인
chain_with_context = rag.create_chain_with_context(retriever)

print("\n" + "="*50)
print("🧪 테스트 실행...")
print("="*50 + "\n")

# 테스트
test_question = "삼성전자가 자체 개발한 생성형 AI의 이름은 무엇인가요?"
#test_result = chain_with_context.invoke(test_question)
#print(f"질문: {test_question}")
#print(f"Context: {test_result['context'][:200]}...")
#print(f"답변: {test_result['answer']}\n")

try:
    test_result = chain_with_context.invoke(test_question)
    print(f"질문: {test_question}")
    print(f"Context: {test_result['context'][:100]}...")
    print(f"답변: {test_result['answer']}\n")
except Exception as e:
    print(f"❌ 테스트 실패: {e}\n")
    import traceback
    traceback.print_exc()
    exit(1)


# ========================================
# Context + Answer 반환 함수
# ========================================

def context_answer_rag_answer(inputs: dict):
    """
    Context와 Answer를 함께 반환
    """
    result = chain_with_context.invoke(inputs["question"])
    return {
        "context": result["context"],
        "answer": result["answer"],
        "query": inputs["question"],
    }

# ========================================
# Labeled Criteria 평가자 생성
# ========================================

print("="*50)
print("📊 Labeled Criteria 평가자 생성...")
print("="*50 + "\n")

# 평가용 LLM 
eval_llm = ChatOllama(
    model="qwen2.5-coder:7b-instruct",
    temperature=0
)

# 1. Helpfulness Evaluator (Ground Truth 기반)
helpfulness_evaluator = LangChainStringEvaluator(
    "labeled_criteria",
    config={
        "criteria": {
            "helpfulness": (
                "Is this submission helpful to the user, "
                "taking into account the correct reference answer?"
            )
        },
        "llm": llm,
    },
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],           # LLM 답변
        "reference": example.outputs["answer"],        # Ground Truth
        "input": example.inputs["question"],           # 질문
    },
)

# 2. Relevance Evaluator (Context 기반)
relevance_evaluator = LangChainStringEvaluator(
    "labeled_criteria",
    config={
        "criteria": "relevance",                # 답변이 Context를 참조하는가?
        "llm": llm,
    },
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],           # LLM 답변
        "reference": run.outputs["context"],           # Context
        "input": example.inputs["question"],           # 질문
    },
)

# 3. Accuracy Evaluator (Ground Truth 기반)
accuracy_evaluator = LangChainStringEvaluator(
    "labeled_criteria",
    config={
        "criteria": {
            "accuracy": (
                "Is this submission factually accurate "
                "compared to the reference answer?"
            )
        },
        "llm": llm,
    },
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],           # LLM 답변
        "reference": example.outputs["answer"],        # Ground Truth
        "input": example.inputs["question"],           # 질문
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
        evaluators=[
            helpfulness_evaluator,
            relevance_evaluator,
            accuracy_evaluator,
        ],
        experiment_prefix="RAG_EVAL_LABELED_CRITERIA_LOCAL",
        metadata={
            "variant": "Labeled Criteria (Helpfulness + Relevance + Accuracy) - Local",
            "k": 10,
            "chunk_size": 300,
            "llm": "qwen2.5-coder:7b-instruct",
        },
        max_concurrency=1,
    )
    
    print("\n" + "="*50)
    print("✅ 평가 완료!")
    print("="*50)
    print(f"\n결과: {experiment_results}\n")
    
except Exception as e:
    print(f"\n❌ 에러 발생: {e}\n")
    import traceback
    traceback.print_exc()