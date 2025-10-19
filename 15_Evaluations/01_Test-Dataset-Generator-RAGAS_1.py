# 01_Test-Dataset-Generator-RAGAS_1.py
"""
llama3.2:3b 교체 및 간단 테스트용
소요 시간: 5-8분
"""
import os
import warnings
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from dotenv import load_dotenv
load_dotenv()

print("="*60)
print("llama3.2:3b 모델 RAGAS 간단 테스트")
print("="*60)
print()

# 패키지 임포트
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset.extractor import KeyphraseExtractor
from ragas.testset.docstore import InMemoryDocumentStore

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ============================================
# 1. LLM 설정
# ============================================
print("1. LLM 설정 중...")

generator_llm = ChatOllama(
    model="llama3.2:3b",                    # 자연어 모델로 교체
    temperature=0.7,
    num_predict=512,
)

# 간단 테스트
try:
    test = generator_llm.invoke("Say hello")
    print(f"    ✅ LLM 작동: {test.content[:30]}...")
except Exception as e:
    print(f"   ❌ 에러: {e}")
    print("   💡 확인: ollama list")
    print("   💡 다운로드: ollama pull llama3.2:3b")
    exit(1)

print()

# ============================================
# 2. Embeddings
# ============================================
print("2. Embeddings 설정 중...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
)
print("    ✅ 완료")
print()

# ============================================
# 3. 문서 로드 (3페이지만!)
# ============================================
print("3. 문서 로드 중...")
loader = PDFPlumberLoader("../data/SPRI_AI_Brief_2023년12월호_F.pdf")
docs = loader.load()[3:6]                       # 3페이지만

for doc in docs:
    doc.metadata["filename"] = doc.metadata["source"]

print(f"    ✅ {len(docs)}페이지 로드")
print()

# ============================================
# 4. DocumentStore
# ============================================
print("4. DocumentStore 초기화 중...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,             # 사이즈 감소
    chunk_overlap=30            # 오버랩 감소
)

langchain_llm = LangchainLLMWrapper(generator_llm)
keyphrase_extractor = KeyphraseExtractor(llm=langchain_llm)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

docstore = InMemoryDocumentStore(
    splitter=splitter,
    embeddings=ragas_embeddings,
    extractor=keyphrase_extractor,
)

print("    ✅ 완료")
print()

# ============================================
# 5. Generator
# ============================================
print("5. Generator 생성 중...")

generator = TestsetGenerator.from_langchain(
    generator_llm,
    generator_llm,
    ragas_embeddings,
    docstore=docstore,
)

print("    ✅ 완료")
print()

# ============================================
# 6. 분포
# ============================================
distributions = {
    simple: 1.0,  # 100% 간단한 질문
}

# ============================================
# 7. 생성 (1개만!)
# ============================================
print("="*60)
print("🔄 테스트셋 생성 시작")
print("="*60)
print("예상 시간: 5-8분")
print("멈춰 보여도 정상입니다!")
print()

try:
    testset = generator.generate_with_langchain_docs(
        documents=docs,
        test_size=1,                        # 1개만!
        distributions=distributions,
        with_debugging_logs=False,
        raise_exceptions=True,
    )
    
    # ============================================
    # 8. 결과
    # ============================================
    test_df = testset.to_pandas()
    
    if len(test_df) > 0:
        print()
        print("="*60)
        print("✅✅✅ 성공! ✅✅✅")
        print("="*60)
        print()
        
        for idx, row in test_df.iterrows():
            print(f"질문: {row['question']}")
            print(f"답변: {row['ground_truth'][:80]}...")
            print()
        
        test_df.to_csv("data/.csv", index=False)
        # test_df.to_csv("data/ragas_synthetic_dataset_1.csv", index=False, encoding='utf-8-sig')
        # 혹은 데이터 경로: "../data/agas_synthetic_dataset_1.csv"
        print("✅ 저장: data/jay_success.csv")

        
    else:
        print("❌ 질문 생성 실패")
        
except Exception as e:
    print()
    print("❌ 에러:")
    print(f"    {e}")
    print()
    print("💡 나에게 에러 메시지 보내줘!")

print()
print("="*60)
print("✅ 테스트셋 생성 완료")
print("="*60)


"""
============================================================
llama3.2:3b 모델 RAGAS 간단 테스트
============================================================

1. LLM 설정 중...
    ✅ LLM 작동: Hello! It's nice to meet you. ...

2. Embeddings 설정 중...
    ✅ 완료

3. 문서 로드 중...
    ✅ 3페이지 로드

4. DocumentStore 초기화 중...
    ✅ 완료

5. Generator 생성 중...
    ✅ 완료

============================================================
🔄 테스트셋 생성 시작
============================================================
예상 시간: 5-8분
멈춰 보여도 정상입니다!

# embedding nodes:  94%|████████████████████████████████████████████████████████████████████████████████▎    | 34/36 [04:09<00:39, 19.87s/it]

# Generating:   0%|                                                                                                    | 0/1 [00:00<?, ?it/s]

============================================================
✅✅✅ 성공! ✅✅✅
============================================================

질문: context: "n \uc8fc\uc694 7\uac1c\uad6d(G7)*\uc740 2023\ub144 10\uc6d4 30\uc77c \u201’\ud788\ub85c\uc2dc\ub9c8 AI \ud504\ub85c\uc138\uc2a4’s\ud97c \ud1b5\ud574 AI \uae30\uc5c5 \ub300\uc0c1\uc758 AI \uad6d\uc81c\n\ud589\ub3d9\uac15\ub839(International Code of Conduct for Advanced AI Systems)\uc5d0 \ud569\uc758\n\u2219 G7\uc740 2023\ub144 5\uc6d4 \uc77c\ubcf8 \ud788\ub85c\uc2dc\ub9c8\uc5d0\uc11c \uac1c\ucd5c\ub41c \uc815\uc0c1\ud68c\uc758\uc5d0\uc11c \uc0dd\uc131 AI\uc5d0 \uad00\ud55c \uad6d\uc81c\uaddc\ubc94 \ub9c8\ub828\acfc\n\uc815\ubcf4\uacf5\uc720\ub97c \uc704\ud574 \u201’\ud788\ub85c\uc2dc\ub9c8 AI \ud504\ub85c\uc138\uc2a4’s\ud97c \ucd9c\ubc94**\n\u2219 \uae30\uc5c5\uc758 \uc790\ubc1c\uc801 \ucc44\ud0dd\uc744 \uc704\ud574 \ub9c8\ub828\ub41c \uc774\ubc88 \ud589\ub3d9\uac15\ub839\uc740 \uae30\ubc18\ubaa8\ub378\acfc \uc0dd\uc131 AI\ud97c \ud3ec\ud568\ud55c \ucca8\ub2e8 AI \uc2dc\uc2a4\ud15c\uc758\n\uc704\ud5d8 \uc2dd\ubcc4\uacfc \uc644\ud654\uc5d
답변: The answer to given question is not present in context...


❌ 에러:
    Cannot save file into a non-existent directory: 'data'

💡 나에게 에러 메시지 보내줘!

============================================================
✅ 테스트셋 생성 완료
============================================================



"""