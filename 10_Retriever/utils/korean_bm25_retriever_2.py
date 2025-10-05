# ========================================
# 🏆 KoreanBM25Retriever (완전 수정 버전)
# ========================================

from kiwipiepy import Kiwi
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from typing import List, Optional, Any
import math

class KoreanBM25Retriever(BaseRetriever):
    """
    Kiwi 형태소 분석기를 사용한 한국어 BM25 검색기
    
    BaseRetriever 상속으로 LangChain Runnable 인터페이스 호환
    
    Features:
    - Kiwi 형태소 분석 기반 토큰화
    - BM25 알고리즘 검색
    - 유사도 점수 계산
    - 검색 결과 개수 조정 (k)
    - EnsembleRetriever 호환 가능
    
    Examples:
        >>> retriever = KoreanBM25Retriever.from_texts(texts)
        >>> results = retriever.invoke("검색어")
        >>> results_with_score = retriever.search_with_score("검색어")
    """
    
    # ========================================
    # Pydantic 설정 ← 추가!
    # ========================================
    class Config:
        """Pydantic 설정"""
        arbitrary_types_allowed = True  # 임의 타입 허용
    
    # ========================================
    # 인스턴스 변수 (클래스 변수 제거!)
    # ========================================
    _retriever: BM25Retriever = None    # ← private 변수로!
    _kiwi: Kiwi = None                  # ← private 변수로!
    _k: int = 4                         # ← private 변수로!
    
    def __init__(
        self,
        retriever: BM25Retriever,
        kiwi: Kiwi,
        k: int = 4,
        **kwargs
    ):
        """
        초기화
        
        Args:
            retriever: BM25Retriever 인스턴스
            kiwi: Kiwi 인스턴스
            k: 반환할 문서 개수
        """
        # BaseRetriever 초기화 (먼저!)
        super().__init__(**kwargs)
        
        # 인스턴스 변수 할당 (나중에!)
        self._retriever = retriever
        self._kiwi = kiwi
        self._k = k
        self._retriever.k = k
    
    # ========================================
    # Property로 접근 (선택사항)
    # ========================================
    
    @property
    def retriever(self) -> BM25Retriever:
        """BM25Retriever 접근"""
        return self._retriever
    
    @property
    def kiwi(self) -> Kiwi:
        """Kiwi 접근"""
        return self._kiwi
    
    @property
    def k(self) -> int:
        """k 값 접근"""
        return self._k
    
    @k.setter
    def k(self, value: int):
        """k 값 설정"""
        self._k = value
        self._retriever.k = value
    
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
        
        # BM25Retriever 생성
        bm25_retriever = BM25Retriever.from_documents(
            docs,
            preprocess_func=korean_tokenizer
        )
        bm25_retriever.k = k
        
        return cls(bm25_retriever, kiwi, k, **kwargs)
    
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
        
        return cls(bm25_retriever, kiwi, k, **kwargs)
    
    # ========================================
    # BaseRetriever 필수 메서드
    # ========================================
    
    def _get_relevant_documents(
        self, 
        query: str,
        *,
        run_manager=None
    ) -> List[Document]:
        """
        BaseRetriever 인터페이스 구현
        
        Args:
            query: 검색 쿼리
            run_manager: 실행 관리자 (선택)
            
        Returns:
            검색된 Document 리스트
        """
        return self._retriever.invoke(query)
    
    # ========================================
    # 추가 메서드들
    # ========================================
    
    def search_with_score(self, query: str) -> List[Document]:
        """
        유사도 점수를 포함한 검색
        
        Args:
            query: 검색 쿼리
            
        Returns:
            점수가 메타데이터에 포함된 Document 리스트
        """
        # 기본 검색 수행
        docs = self._get_relevant_documents(query)
        
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
        tokens = self._kiwi.tokenize(text)
        meaningful_tags = ['NNG', 'NNP', 'VV', 'VA', 'SL', 'SH']
        return [
            token.form for token in tokens 
            if token.tag in meaningful_tags and len(token.form) > 1
        ]


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
