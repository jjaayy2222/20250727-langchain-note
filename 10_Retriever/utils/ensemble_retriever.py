# utils/ensemble_retriever.py

# ========================================
# 🏆 Custom Ensemble Retriever
# RRF & CC 알고리즘 완전 구현
# ========================================

from enum import Enum
from typing import List, Optional, Dict, Tuple
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
import numpy as np


class EnsembleMethod(Enum):
    """앙상블 방법 Enum"""
    RRF = "rrf"  # Reciprocal Rank Fusion
    CC = "cc"    # Convex Combination


class CustomEnsembleRetriever(BaseRetriever):
    """
    커스텀 앙상블 리트리버 (RRF & CC 지원)
    
    Features:
    - RRF (Reciprocal Rank Fusion): 순위 기반 결합
    - CC (Convex Combination): 점수 기반 가중 결합
    - 가중치 조정 가능
    - BaseRetriever 상속으로 LCEL 호환
    
    Examples:
        >>> # RRF 방식
        >>> ensemble = CustomEnsembleRetriever(
        ...     retrievers=[faiss, bm25],
        ...     method=EnsembleMethod.RRF
        ... )
        
        >>> # CC 방식 (가중치 조정)
        >>> ensemble = CustomEnsembleRetriever(
        ...     retrievers=[faiss, bm25],
        ...     method=EnsembleMethod.CC,
        ...     weights=[0.7, 0.3]
        ... )
    """
    
    # ========================================
    # Pydantic 설정
    # ========================================
    class Config:
        arbitrary_types_allowed = True
    
    # ========================================
    # 인스턴스 변수
    # ========================================
    _retrievers: List[BaseRetriever] = []
    _method: EnsembleMethod = EnsembleMethod.RRF
    _weights: Optional[List[float]] = None
    _k: int = 5
    _c: int = 60  # RRF constant
    
    def __init__(
        self,
        retrievers: List[BaseRetriever],
        method: EnsembleMethod = EnsembleMethod.RRF,
        weights: Optional[List[float]] = None,
        k: int = 5,
        c: int = 60,
        **kwargs
    ):
        """
        초기화
        
        Args:
            retrievers: 검색기 리스트
            method: 앙상블 방법 (RRF 또는 CC)
            weights: 각 검색기의 가중치 (CC에서만 사용)
            k: 반환할 문서 개수
            c: RRF 상수 (기본 60)
        """
        super().__init__(**kwargs)
        
        self._retrievers = retrievers
        self._method = method
        self._k = k
        self._c = c
        
        # 가중치 설정
        if weights is None:
            # 균등 가중치
            self._weights = [1.0 / len(retrievers)] * len(retrievers)
        else:
            if len(weights) != len(retrievers):
                raise ValueError(
                    f"weights 길이({len(weights)})가 "
                    f"retrievers 길이({len(retrievers)})와 다릅니다."
                )
            # 정규화
            total = sum(weights)
            self._weights = [w / total for w in weights]
    
    # ========================================
    # Property
    # ========================================
    
    @property
    def method(self) -> EnsembleMethod:
        return self._method
    
    @property
    def weights(self) -> List[float]:
        return self._weights
    
    @property
    def k(self) -> int:
        return self._k
    
    @k.setter
    def k(self, value: int):
        self._k = value
    
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
        앙상블 검색 실행
        
        Args:
            query: 검색 쿼리
            run_manager: 실행 관리자
            
        Returns:
            앙상블된 Document 리스트
        """
        # 각 검색기에서 문서 검색
        retriever_docs = []
        for retriever in self._retrievers:
            docs = retriever.invoke(query)
            retriever_docs.append(docs)
        
        # 앙상블 방법에 따라 결합
        if self._method == EnsembleMethod.RRF:
            return self._rrf_fusion(retriever_docs)
        elif self._method == EnsembleMethod.CC:
            return self._cc_fusion(retriever_docs, query)
        else:
            raise ValueError(f"알 수 없는 method: {self._method}")
    
    # ========================================
    # RRF 알고리즘 구현
    # ========================================
    
    def _rrf_fusion(
        self,
        retriever_docs: List[List[Document]]
    ) -> List[Document]:
        """
        Reciprocal Rank Fusion (RRF)
        
        공식: RRF_score(d) = Σ 1 / (k + rank_i(d))
        - k: 상수 (기본 60)
        - rank_i(d): i번째 검색기에서 문서 d의 순위
        
        Args:
            retriever_docs: 각 검색기의 Document 리스트
            
        Returns:
            RRF로 결합된 Document 리스트
        """
        # 문서별 RRF 점수 계산
        doc_scores: Dict[str, Tuple[Document, float]] = {}
        
        for retriever_idx, docs in enumerate(retriever_docs):
            for rank, doc in enumerate(docs, start=1):
                # 문서 식별자 (content로 구분)
                doc_id = doc.page_content
                
                # RRF 점수 계산: 1 / (c + rank)
                rrf_score = 1.0 / (self._c + rank)
                
                if doc_id in doc_scores:
                    # 기존 점수에 추가
                    existing_doc, existing_score = doc_scores[doc_id]
                    doc_scores[doc_id] = (existing_doc, existing_score + rrf_score)
                else:
                    # 새 문서 추가
                    doc_scores[doc_id] = (doc, rrf_score)
        
        # 점수 기준 정렬
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 상위 k개 반환
        return [doc for doc, _ in sorted_docs[:self._k]]
    
    # ========================================
    # CC 알고리즘 구현
    # ========================================
    
    def _cc_fusion(
        self,
        retriever_docs: List[List[Document]],
        query: str
    ) -> List[Document]:
        """
        Convex Combination (CC)
        
        공식: CC_score(d) = Σ w_i * score_i(d)
        - w_i: i번째 검색기의 가중치
        - score_i(d): i번째 검색기에서 문서 d의 유사도 점수
        
        Args:
            retriever_docs: 각 검색기의 Document 리스트
            query: 검색 쿼리
            
        Returns:
            CC로 결합된 Document 리스트
        """
        # 문서별 CC 점수 계산
        doc_scores: Dict[str, Tuple[Document, float]] = {}
        
        for retriever_idx, docs in enumerate(retriever_docs):
            weight = self._weights[retriever_idx]
            
            # 각 검색기의 점수를 정규화 (0~1)
            scores = self._normalize_scores(docs, query)
            
            for doc, score in zip(docs, scores):
                doc_id = doc.page_content
                
                # CC 점수 계산: w_i * score_i
                weighted_score = weight * score
                
                if doc_id in doc_scores:
                    existing_doc, existing_score = doc_scores[doc_id]
                    doc_scores[doc_id] = (
                        existing_doc, 
                        existing_score + weighted_score
                    )
                else:
                    doc_scores[doc_id] = (doc, weighted_score)
        
        # 점수 기준 정렬
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 상위 k개 반환
        return [doc for doc, _ in sorted_docs[:self._k]]
    
    # ========================================
    # 점수 정규화
    # ========================================
    
    def _normalize_scores(
        self,
        docs: List[Document],
        query: str
    ) -> List[float]:
        """
        문서 점수를 0~1로 정규화
        
        Args:
            docs: Document 리스트
            query: 검색 쿼리
            
        Returns:
            정규화된 점수 리스트
        """
        # 메타데이터에 score가 있으면 사용
        scores = []
        for doc in docs:
            if 'score' in doc.metadata:
                scores.append(doc.metadata['score'])
            else:
                # score가 없으면 순위 기반으로 점수 생성
                # 1위 = 1.0, 2위 = 0.9, 3위 = 0.8, ...
                rank = len(scores) + 1
                score = 1.0 - (rank - 1) * 0.1
                scores.append(max(score, 0.1))  # 최소 0.1
        
        # Min-Max 정규화
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            # 모든 점수가 같으면 균등
            return [1.0 / len(scores)] * len(scores)
        
        # 0~1 범위로 정규화
        normalized = [
            (score - min_score) / (max_score - min_score)
            for score in scores
        ]
        
        return normalized
    
    # ========================================
    # 추가 유틸리티
    # ========================================
    
    def get_scores(self, query: str) -> List[Tuple[Document, float]]:
        """
        점수와 함께 문서 반환
        
        Args:
            query: 검색 쿼리
            
        Returns:
            (Document, score) 튜플 리스트
        """
        # 각 검색기에서 문서 검색
        retriever_docs = []
        for retriever in self._retrievers:
            docs = retriever.invoke(query)
            retriever_docs.append(docs)
        
        # 점수 계산
        doc_scores: Dict[str, Tuple[Document, float]] = {}
        
        if self._method == EnsembleMethod.RRF:
            # RRF 점수
            for retriever_idx, docs in enumerate(retriever_docs):
                for rank, doc in enumerate(docs, start=1):
                    doc_id = doc.page_content
                    rrf_score = 1.0 / (self._c + rank)
                    
                    if doc_id in doc_scores:
                        existing_doc, existing_score = doc_scores[doc_id]
                        doc_scores[doc_id] = (existing_doc, existing_score + rrf_score)
                    else:
                        doc_scores[doc_id] = (doc, rrf_score)
        
        elif self._method == EnsembleMethod.CC:
            # CC 점수
            for retriever_idx, docs in enumerate(retriever_docs):
                weight = self._weights[retriever_idx]
                scores = self._normalize_scores(docs, query)
                
                for doc, score in zip(docs, scores):
                    doc_id = doc.page_content
                    weighted_score = weight * score
                    
                    if doc_id in doc_scores:
                        existing_doc, existing_score = doc_scores[doc_id]
                        doc_scores[doc_id] = (existing_doc, existing_score + weighted_score)
                    else:
                        doc_scores[doc_id] = (doc, weighted_score)
        
        # 점수 기준 정렬
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_docs[:self._k]


# ========================================
# 🎯 예쁜 출력 함수
# ========================================

def pretty_print_ensemble(docs: List[Document], method_name: str = ""):
    """
    앙상블 검색 결과 예쁘게 출력
    
    Args:
        docs: Document 리스트
        method_name: 방법 이름 (출력용)
    """
    if method_name:
        print(f"\n{'='*60}")
        print(f"📊 {method_name}")
        print(f"{'='*60}")
    
    for i, doc in enumerate(docs, start=1):
        print(f"\n[{i}] {doc.page_content[:80]}...")
        if 'score' in doc.metadata:
            print(f"    점수: {doc.metadata['score']:.4f}")


def compare_methods(
    retrievers: List[BaseRetriever],
    query: str,
    k: int = 5
):
    """
    RRF vs CC 비교 출력
    
    Args:
        retrievers: 검색기 리스트
        query: 검색 쿼리
        k: 반환 문서 수
    """
    print(f"\n{'='*60}")
    print(f"🔍 검색어: {query}")
    print(f"{'='*60}")
    
    # RRF
    rrf_ensemble = CustomEnsembleRetriever(
        retrievers=retrievers,
        method=EnsembleMethod.RRF,
        k=k
    )
    rrf_results = rrf_ensemble.invoke(query)
    rrf_scores = rrf_ensemble.get_scores(query)
    
    # CC
    cc_ensemble = CustomEnsembleRetriever(
        retrievers=retrievers,
        method=EnsembleMethod.CC,
        k=k
    )
    cc_results = cc_ensemble.invoke(query)
    cc_scores = cc_ensemble.get_scores(query)
    
    # 출력
    print("\n" + "="*60)
    print("📊 RRF (Reciprocal Rank Fusion)")
    print("="*60)
    for i, (doc, score) in enumerate(rrf_scores, start=1):
        print(f"\n[{i}] 점수: {score:.4f}")
        print(f"    {doc.page_content[:80]}...")
    
    print("\n" + "="*60)
    print("📊 CC (Convex Combination)")
    print("="*60)
    for i, (doc, score) in enumerate(cc_scores, start=1):
        print(f"\n[{i}] 점수: {score:.4f}")
        print(f"    {doc.page_content[:80]}...")
    
    # 차이 분석
    print("\n" + "="*60)
    print("📊 차이 분석")
    print("="*60)
    
    if rrf_results[0].page_content == cc_results[0].page_content:
        print("\n✅ RRF와 CC가 동일한 1위 선택")
    else:
        print("\n⚠️ RRF와 CC가 다른 1위 선택!")
        print(f"\nRRF 1위: {rrf_results[0].page_content[:60]}...")
        print(f"CC 1위:  {cc_results[0].page_content[:60]}...")
