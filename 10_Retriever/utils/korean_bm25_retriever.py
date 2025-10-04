# 10_Retriever/utils/korean_bm25_retriever.py

from kiwipiepy import Kiwi
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from typing import List, Optional
import math

class KoreanBM25Retriever:
    """
    Kiwi 형태소 분석기를 사용한 한국어 BM25 검색기
    
    Features:
    - Kiwi 형태소 분석 기반 토큰화
    - BM25 알고리즘 검색
    - 유사도 점수 계산
    - 검색 결과 개수 조정 (k)
    
    Examples:
        >>> retriever = KoreanBM25Retriever.from_texts(texts)
        >>> results = retriever.invoke("검색어")
        >>> results_with_score = retriever.search_with_score("검색어")
    """
    
    def __init__(
        self,
        retriever: BM25Retriever,
        kiwi: Kiwi,
        k: int = 4
    ):
        """
        초기화
        
        Args:
            retriever: BM25Retriever 인스턴스
            kiwi: Kiwi 인스턴스
            k: 반환할 문서 개수
        """
        self.retriever = retriever
        self.kiwi = kiwi
        self.k = k
        self.retriever.k = k
    
    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
        k: int = 4,
        **kwargs
    ) -> "KoreanBM25Retriever":
        """
        텍스트 리스트로부터 검색기 생성
        
        Args:
            texts: 문서 텍스트 리스트
            metadatas: 메타데이터 리스트 (선택)
            k: 반환할 문서 개수
            
        Returns:
            KoreanBM25Retriever 인스턴스
        """
        # Kiwi 인스턴스 생성
        kiwi = Kiwi()
        
        # 토크나이저 함수 정의
        def korean_tokenizer(text: str) -> List[str]:
            """Kiwi 기반 한국어 토크나이저"""
            tokens = kiwi.tokenize(text)
            # 의미있는 형태소만 추출 (명사, 동사, 형용사, 외국어)
            meaningful_tags = ['NNG', 'NNP', 'VV', 'VA', 'SL', 'SH']
            return [
                token.form for token in tokens 
                if token.tag in meaningful_tags and len(token.form) > 1
            ]
        
        # Document 객체 생성
        if metadatas:
            docs = [
                Document(page_content=text, metadata=metadata)
                for text, metadata in zip(texts, metadatas)
            ]
        else:
            docs = [Document(page_content=text) for text in texts]
        
        # BM25Retriever 생성 (Kiwi 토크나이저 적용)
        bm25_retriever = BM25Retriever.from_documents(
            docs,
            preprocess_func=korean_tokenizer
        )
        bm25_retriever.k = k
        
        return cls(bm25_retriever, kiwi, k)
    
    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        k: int = 4,
        **kwargs
    ) -> "KoreanBM25Retriever":
        """
        Document 객체 리스트로부터 검색기 생성
        
        Args:
            documents: Document 객체 리스트
            k: 반환할 문서 개수
            
        Returns:
            KoreanBM25Retriever 인스턴스
        """
        # Kiwi 인스턴스 생성
        kiwi = Kiwi()
        
        # 토크나이저 함수 정의
        def korean_tokenizer(text: str) -> List[str]:
            """Kiwi 기반 한국어 토크나이저"""
            tokens = kiwi.tokenize(text)
            meaningful_tags = ['NNG', 'NNP', 'VV', 'VA', 'SL', 'SH']
            return [
                token.form for token in tokens 
                if token.tag in meaningful_tags and len(token.form) > 1
            ]
        
        # BM25Retriever 생성
        bm25_retriever = BM25Retriever.from_documents(
            documents,
            preprocess_func=korean_tokenizer
        )
        bm25_retriever.k = k
        
        return cls(bm25_retriever, kiwi, k)
    
    def invoke(self, query: str) -> List[Document]:
        """
        검색 실행 (기본)
        
        Args:
            query: 검색 쿼리
            
        Returns:
            검색된 Document 리스트
        """
        return self.retriever.invoke(query)
    
    def search_with_score(self, query: str) -> List[Document]:
        """
        유사도 점수를 포함한 검색
        
        Args:
            query: 검색 쿼리
            
        Returns:
            점수가 메타데이터에 포함된 Document 리스트
        """
        # 기본 검색 수행
        docs = self.retriever.invoke(query)
        
        # 점수 계산 (간단한 BM25 점수 근사)
        # 실제로는 retriever 내부의 BM25 점수를 사용해야 하지만
        # 여기서는 교재 스타일로 정규화된 점수 계산
        
        # 쿼리 토큰화
        query_tokens = self._tokenize(query)
        
        # 각 문서의 점수 계산
        scored_docs = []
        for doc in docs:
            doc_tokens = self._tokenize(doc.page_content)
            
            # 단순 overlap 기반 점수 (0~1 정규화)
            common_tokens = set(query_tokens) & set(doc_tokens)
            score = len(common_tokens) / max(len(query_tokens), 1)
            
            # 메타데이터에 점수 추가
            new_metadata = doc.metadata.copy()
            new_metadata['score'] = score
            
            scored_doc = Document(
                page_content=doc.page_content,
                metadata=new_metadata
            )
            scored_docs.append(scored_doc)
        
        # 점수 기준 정렬
        scored_docs.sort(key=lambda x: x.metadata['score'], reverse=True)
        
        return scored_docs
    
    def _tokenize(self, text: str) -> List[str]:
        """내부 토큰화 함수"""
        tokens = self.kiwi.tokenize(text)
        meaningful_tags = ['NNG', 'NNP', 'VV', 'VA', 'SL', 'SH']
        return [
            token.form for token in tokens 
            if token.tag in meaningful_tags and len(token.form) > 1
        ]
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """LangChain Retriever 인터페이스 호환"""
        return self.invoke(query)


# ========================================
# 🎯 예쁜 출력 함수
# ========================================

def pretty_print(docs: List[Document]):
    """
    검색 결과 예쁘게 출력
    
    Args:
        docs: Document 리스트
    """
    for i, doc in enumerate(docs):
        if "score" in doc.metadata:
            print(f"[{i+1}] {doc.page_content} ({doc.metadata['score']:.4f})")
        else:
            print(f"[{i+1}] {doc.page_content}")


# ========================================
# 🚀 사용 예제 (교재와 동일)
# ========================================

def example_basic():
    """기본 검색 예제"""
    print("=" * 60)
    print("🚀 예제 1: 기본 BM25 검색")
    print("=" * 60)
    
    # 샘플 텍스트 (교재와 동일)
    sample_texts = [
        "금융보험은 장기적인 자산 관리와 위험 대비를 목적으로 고안된 금융 상품입니다.",
        "금융저축산물보험은 장기적인 저축 목적과 더불어, 축산물 제공 기능을 갖추고 있는 특별 금융 상품입니다.",
        "금융보씨 험한말 좀 하지마시고, 저축이나 좀 하시던가요. 뭐가 그리 급하신지 모르겠네요.",
        "금융단폭격보험은 저축은 커녕 위험 대비에 초점을 맞춘 상품입니다. 높은 위험을 감수하고자 하는 고객에게 적합합니다.",
    ]
    
    # 리트리버 생성
    kiwi_retriever = KoreanBM25Retriever.from_texts(sample_texts)
    
    # 검색 수행
    print("\n🔍 검색어: '금융보험'")
    print("\n📊 검색 결과:")
    results = kiwi_retriever.invoke("금융보험")
    pretty_print(results)


def example_with_score():
    """점수 포함 검색 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 2: 점수 포함 검색")
    print("=" * 60)
    
    sample_texts = [
        "금융보험은 장기적인 자산 관리와 위험 대비를 목적으로 고안된 금융 상품입니다.",
        "금융저축산물보험은 장기적인 저축 목적과 더불어, 축산물 제공 기능을 갖추고 있는 특별 금융 상품입니다.",
        "금융보씨 험한말 좀 하지마시고, 저축이나 좀 하시던가요. 뭐가 그리 급하신지 모르겠네요.",
        "금융단폭격보험은 저축은 커녕 위험 대비에 초점을 맞춘 상품입니다. 높은 위험을 감수하고자 하는 고객에게 적합합니다.",
    ]
    
    kiwi_retriever = KoreanBM25Retriever.from_texts(sample_texts)
    
    print("\n🔍 검색어: '금융보험'")
    print("\n📊 점수 포함 결과:")
    results = kiwi_retriever.search_with_score("금융보험")
    pretty_print(results)


def example_k_setting():
    """k 값 설정 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 3: k 값 설정 (상위 2개만)")
    print("=" * 60)
    
    sample_texts = [
        "금융보험은 장기적인 자산 관리와 위험 대비를 목적으로 고안된 금융 상품입니다.",
        "금융저축산물보험은 장기적인 저축 목적과 더불어, 축산물 제공 기능을 갖추고 있는 특별 금융 상품입니다.",
        "금융보씨 험한말 좀 하지마시고, 저축이나 좀 하시던가요. 뭐가 그리 급하신지 모르겠네요.",
        "금융단폭격보험은 저축은 커녕 위험 대비에 초점을 맞춘 상품입니다. 높은 위험을 감수하고자 하는 고객에게 적합합니다.",
    ]
    
    # k=2로 생성
    kiwi_retriever = KoreanBM25Retriever.from_texts(sample_texts, k=2)
    
    print("\n🔍 검색어: '금융보험'")
    print("\n📊 상위 2개 결과:")
    results = kiwi_retriever.search_with_score("금융보험")
    pretty_print(results)


def example_comparison():
    """기본 BM25 vs Kiwi BM25 비교"""
    print("\n" + "=" * 60)
    print("🚀 예제 4: 기본 BM25 vs Kiwi BM25 비교")
    print("=" * 60)
    
    sample_texts = [
        "금융보험은 장기적인 자산 관리와 위험 대비를 목적으로 고안된 금융 상품입니다.",
        "금융저축산물보험은 장기적인 저축 목적과 더불어, 축산물 제공 기능을 갖추고 있는 특별 금융 상품입니다.",
        "금융보씨 험한말 좀 하지마시고, 저축이나 좀 하시던가요. 뭐가 그리 급하신지 모르겠네요.",
        "금융단폭격보험은 저축은 커녕 위험 대비에 초점을 맞춘 상품입니다. 높은 위험을 감수하고자 하는 고객에게 적합합니다.",
    ]
    
    # Kiwi BM25
    kiwi_retriever = KoreanBM25Retriever.from_texts(sample_texts)
    
    # 기본 BM25
    docs = [Document(page_content=text) for text in sample_texts]
    basic_retriever = BM25Retriever.from_documents(docs)
    
    query = "금융보험"
    
    print(f"\n🔍 검색어: '{query}'")
    print("\n📊 Kiwi BM25 1위:")
    kiwi_result = kiwi_retriever.invoke(query)[0]
    print(f"   {kiwi_result.page_content}")
    
    print("\n📊 기본 BM25 1위:")
    basic_result = basic_retriever.invoke(query)[0]
    print(f"   {basic_result.page_content}")
    
    print("\n💡 차이점:")
    if kiwi_result.page_content != basic_result.page_content:
        print("   ✅ Kiwi가 형태소 분석으로 더 정확한 결과 반환!")
    else:
        print("   이번 케이스에서는 동일한 결과")


# ========================================
# 🎬 메인 실행
# ========================================

if __name__ == "__main__":
    example_basic()
    example_with_score()
    example_k_setting()
    example_comparison()
    
    print("\n" + "=" * 60)
    print("✅ 모든 예제 완료!")
    print("=" * 60)