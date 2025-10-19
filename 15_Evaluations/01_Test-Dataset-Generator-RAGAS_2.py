# 01_Test-Dataset-Generator-RAGAS_2.py

"""
RAGAS 테스트셋 생성 - 빠른 테스트용
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

print("🔧 RAGAS 초기화 중...\n")

from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset.extractor import KeyphraseExtractor
from ragas.testset.docstore import InMemoryDocumentStore

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. LLM 설정 (온도 0.1로 조금 높임 - 더 안정적)
print("1. LLM 설정 중...")

generator_llm = ChatOllama(
    model="llama3.2:3b",                    # 자연어 모델로 교체
    temperature=0.7,
    num_predict=512,
)

critic_llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.1,
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


print("    ✅ Ollama LLM 설정 완료")
print()


# 2. Embeddings 설정
print("2. Embeddings 설정 중...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

print("    ✅ 완료")
print()


# 3. 문서 로드
print("3. 문서 로드 중...")
loader = PDFPlumberLoader("data/SPRI_AI_Brief_2023년12월호_F.pdf")
docs = loader.load()
docs = docs[3:8]                            # 5페이지만!

# metadata 설정
for doc in docs:
    doc.metadata["filename"] = doc.metadata["source"]

print(f"    ✅ {len(docs)}페이지 로드")
print()


# 4. DocumentStore 초기화
print("4. DocumentStore 초기화 중...")

splitter = RecursiveCharacterTextSplitter(
    #chunk_size=800,            # 조금 줄임
    #chunk_size=400,            # 더 작게 조절
    #chunk_overlap=50 
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


# 5. TestsetGenerator 생성
print("5. Generator 생성 중...")

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    ragas_embeddings,
    docstore=docstore,
)

print("    ✅ 완료")
print()


# 6. 분포 (간단하게!)
distributions = {
    simple: 0.7,      # 70%
    reasoning: 0.3,   # 30%
}


# 7. 생성 (2개만!)
print("="*60)
print("🔄 테스트셋 생성 시작")
print("="*60)
print("🔄 테스트셋 생성 중... (시간이 걸릴 수 있습니다)")
print("    - 분포: 간단(70%), 추론(30%)\n")
print("🔄 멈춰 보여도 정상입니다! 🔄 ")
print("="*60)
print()

try:
    testset = generator.generate_with_langchain_docs(
        documents=docs,
        test_size=2,                        # 2개만
        distributions=distributions,
        with_debugging_logs=False,          # 로그 비활성화
        raise_exceptions=False,             # 에러 무시
    )
    
    # 8. 결과 저장
    test_df = testset.to_pandas()
    test_df.to_csv("data/ragas_synthetic_dataset_2.csv", index=False, encoding='utf-8-sig')
    
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
        
        #test_df.to_csv("data/.csv", index=False, encoding='utf-8-sig')
        #test_df.to_csv("data/ragas_synthetic_dataset_2.csv", index=False, encoding='utf-8-sig')
        print("✅ 저장: data/ragas_synthetic_dataset_2.csv")

    else:
        print("❌ 질문 생성 실패")

    print()
    print("="*60)  
    print(f"\n✅ 테스트셋 생성 완료!")
    print(f"   - 생성된 질문 수: {len(test_df)}")
    print(f"   - 저장 위치: ../15_Evaluations/data/ragas_synthetic_dataset.csv\n")
    print(test_df)
    
    # 9. 결과 미리보기
    print("📊 생성된 질문 미리보기:")
    print("="*80)
    for idx, row in test_df.iterrows():
        print(f"\n질문 {idx+1}:")
        print(f"  {row['question']}")
        print(f"  Ground Truth: {row['ground_truth'][:100]}...")
    
except Exception as e:
    print(f"❌ 에러 발생: {e}")
    print("\n💡 해결 방법:")
    print("    1. Ollama가 실행 중인지 확인")
    print("    2. 모델 다운로드: ollama pull llama3.2:3b")
    print("    3. langchain-ollama 버전 확인: pip list | grep langchain-ollama")
    print("        → 0.1.3이어야 함!")

print("\n✅ 정상적으로 테스트셋 생성 완료!")


"""
try_1
    🔧 RAGAS 초기화 중...

    ✅ Ollama LLM 설정 완료
    ✅ Embeddings 설정 완료
    ✅ 문서 로드 완료: 5페이지

    ✅ TestsetGenerator 생성 완료

    🔄 시작... (10분 예상)
    🔄 테스트셋 생성 중... (시간이 걸릴 수 있습니다)
        - 분포: 간단(70%), 추론(30%)
        
    # embedding nodes:  37%|██████████████████████████▌                                             | 17/46 [00:33<01:46,  3.68s/it]
    # embedding nodes:  87%|██████████████████████████████████████████████████████████████▌         | 40/46 [06:56<02:35, 25.91s/it]
    # embedding nodes:  98%|██████████████████████████████████████████████████████████████████████▍ | 45/46 [09:26<00:29, 29.29s/it]

    # Generating:   0%|                                                                                       | 0/2 [00:00<?, ?it/s]
    # Generating:  50%|███████████████████████████████████████                                       | 1/2 [06:24<06:24, 384.85s/it]

    Generating:  50%|███████████████████████████████████████                                       | 1/2 [06:24<06:24, 384.85s/itFailed to parse output. Returning None.
    ↳ 멈춤 → 강제종료    

"""

""" 
try_2

============================================================
llama3.2:3b 모델 RAGAS 간단 테스트
============================================================

🔧 RAGAS 초기화 중...

1. LLM 설정 중...
    ✅ LLM 작동: Hello! It's nice to meet you. ...
    ✅ Ollama LLM 설정 완료

2. Embeddings 설정 중...
    ✅ 완료

3. 문서 로드 중...
    ✅ 5페이지 로드

4. DocumentStore 초기화 중...
    ✅ 완료

5. Generator 생성 중...
    ✅ 완료

============================================================
🔄 테스트셋 생성 시작
============================================================
🔄 테스트셋 생성 중... (시간이 걸릴 수 있습니다)
    - 분포: 간단(70%), 추론(30%)

🔄 멈춰 보여도 정상입니다! 🔄 
============================================================

# embedding nodes:  26%|█████████████████████▏                                                            | 15/58 [00:44<03:09,  4.40s/it
# embedding nodes:  74%|████████████████████████████████████████████████████████████▊                     | 43/58 [04:51<02:06,  8.45s/it]
# embedding nodes:  93%|████████████████████████████████████████████████████████████████████████████▎     | 54/58 [09:42<01:50, 27.70s/it]

# Generating:   0%|                                                                                                 | 0/2 [00:00<?, ?it/s]
# Generating:  50%|████████████████████████████████████████████                                            | 1/2 [07:46<07:46, 466.04s/it]

Generating: 100%|████████████████████████████████████████████████████████████████████████████████████████| 2/2 [22:33<00:00, 676.72s/it]

============================================================
✅✅✅ 성공! ✅✅✅
============================================================

질문: Here is a question that can be fully answered from the given context:

"What does 'FTC' stand for in the provided text?"

This question can be answered by referring to the key phrase "KEY Contents\nn \ubbf8\uad6d FTC..." in the context, which explicitly states what "FTC" stands for.
답변: FTC...

질문: The goal is to create a rewritten question that conveys the same meaning as "What type of AI does the Federal Trade Commission possess?" without directly stating it.

Here's a revised version:

"What kind of AI system does the FTC use?"

This rewritten question achieves the same intent as the original but in a more concise and indirect manner, using abbreviation ("FTC" instead of "Federal Trade Commission") to make the question shorter.
답변: The Federal Trade Commission uses artificial intelligence primarily for regulati...

✅ 저장: data/ragas_synthetic_dataset_2.csv

============================================================

✅ 테스트셋 생성 완료!
    - 생성된 질문 수: 2
    - 저장 위치: ../15_Evaluations/data/ragas_synthetic_dataset.csv

                                            question  ... episode_done
0  Here is a question that can be fully answered ...  ...         True
1  The goal is to create a rewritten question tha...  ...         True

[2 rows x 6 columns]
📊 생성된 질문 미리보기:
================================================================================

질문 1:
  Here is a question that can be fully answered from the given context:

"What does 'FTC' stand for in the provided text?"

This question can be answered by referring to the key phrase "KEY Contents\nn \ubbf8\uad6d FTC..." in the context, which explicitly states what "FTC" stands for.
  Ground Truth: FTC...

질문 2:
  The goal is to create a rewritten question that conveys the same meaning as "What type of AI does the Federal Trade Commission possess?" without directly stating it.

Here's a revised version:

"What kind of AI system does the FTC use?"

This rewritten question achieves the same intent as the original but in a more concise and indirect manner, using abbreviation ("FTC" instead of "Federal Trade Commission") to make the question shorter.
  Ground Truth: The Federal Trade Commission uses artificial intelligence primarily for regulating privacy, trademar...

✅ 정상적으로 테스트셋 생성 완료!

"""
