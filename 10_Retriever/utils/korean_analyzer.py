# 10_Retriever/utils/korean_analyzer.py

# ========================================
# 🏆 Korean Morphological Analyzer Class
# 한국어 형태소 분석 통합 모델
# ========================================

from kiwipiepy import Kiwi
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TokenInfo:
    """토큰 정보를 담는 데이터 클래스"""
    form: str              # 형태소
    tag: str               # 품사 태그
    score: float           # 로그 확률
    probability: float     # 확률 (0~1)
    start: int            # 시작 위치
    length: int           # 길이
    tagged_form: str      # 형태소/품사

class KoreanMorphologicalAnalyzer:
    """
    한국어 형태소 분석 통합 클래스
    
    Features:
    - 형태소 분석
    - 신뢰도 기반 필터링
    - 품사별 토큰 추출
    - 상세 정보 조회
    
    Examples:
        >>> analyzer = KoreanMorphologicalAnalyzer()
        >>> result = analyzer.analyze("안녕하세요")
        >>> keywords = analyzer.extract_keywords("Python은 좋은 언어입니다", confidence=-10.0)
    """
    
    # 품사 태그 설명
    POS_TAGS = {
        'NNG': '일반 명사',
        'NNP': '고유 명사',
        'NNB': '의존 명사',
        'VV': '동사',
        'VA': '형용사',
        'MM': '관형사',
        'MAG': '일반 부사',
        'XR': '어근',
        'SL': '외국어',
        'SH': '한자',
        'JKS': '주격 조사',
        'JKO': '목적격 조사',
        'JKB': '부사격 조사',
        'EP': '선어말 어미',
        'EF': '종결 어미',
        'EC': '연결 어미',
        'XSV': '동사 파생 접미사',
        'XSA': '형용사 파생 접미사',
        'SP': '쉼표, 가운뎃점, 콜론, 빗금',
        'SF': '마침표, 물음표, 느낌표',
    }
    
    # 의미있는 품사 (키워드 추출용)
    MEANINGFUL_TAGS = ['NNG', 'NNP', 'VV', 'VA', 'SL', 'SH', 'MM', 'MAG']
    
    def __init__(
        self, 
        model_type: str = 'sbg',
        typos: str = 'basic',
        load_default_dict: bool = True
    ):
        """
        초기화
        
        Args:
            model_type: 모델 타입 ('sbg', 'knlm')
            typos: 오타 교정 수준 ('basic', 'auto', 'disabled')
            load_default_dict: 기본 사전 로드 여부
        """
        self.kiwi = Kiwi(
            model_type=model_type,
            typos=typos,
            load_default_dict=load_default_dict
        )
        self.last_analysis = None
    
    def analyze(self, text: str) -> List[TokenInfo]:
        """
        텍스트 형태소 분석
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            TokenInfo 객체 리스트
        """
        tokens = self.kiwi.tokenize(text)
        
        result = []
        for token in tokens:
            result.append(TokenInfo(
                form=token.form,
                tag=token.tag,
                score=token.score,
                probability=math.exp(token.score),
                start=token.start,
                length=token.len,
                tagged_form=token.tagged_form
            ))
        
        self.last_analysis = result
        return result
    
    def extract_keywords(
        self, 
        text: str, 
        confidence_threshold: float = -10.0,
        pos_tags: Optional[List[str]] = None
    ) -> List[str]:
        """
        신뢰도 기반 키워드 추출
        
        Args:
            text: 분석할 텍스트
            confidence_threshold: 신뢰도 임계값 (낮을수록 엄격)
            pos_tags: 추출할 품사 태그 (기본: MEANINGFUL_TAGS)
            
        Returns:
            추출된 키워드 리스트
        """
        if pos_tags is None:
            pos_tags = self.MEANINGFUL_TAGS
        
        tokens = self.analyze(text)
        
        keywords = [
            token.form for token in tokens
            if token.score > confidence_threshold and token.tag in pos_tags
        ]
        
        return keywords
    
    def extract_by_pos(self, text: str, pos_tag: str) -> List[str]:
        """
        특정 품사만 추출
        
        Args:
            text: 분석할 텍스트
            pos_tag: 품사 태그 ('NNG', 'VV' 등)
            
        Returns:
            해당 품사의 형태소 리스트
        """
        tokens = self.analyze(text)
        return [token.form for token in tokens if token.tag == pos_tag]
    
    def extract_nouns(self, text: str) -> List[str]:
        """명사만 추출 (일반명사 + 고유명사)"""
        tokens = self.analyze(text)
        return [token.form for token in tokens if token.tag in ['NNG', 'NNP']]
    
    def extract_verbs(self, text: str) -> List[str]:
        """동사만 추출"""
        return self.extract_by_pos(text, 'VV')
    
    def extract_adjectives(self, text: str) -> List[str]:
        """형용사만 추출"""
        return self.extract_by_pos(text, 'VA')
    
    def get_detailed_info(self, text: str) -> List[Dict]:
        """
        상세 정보 포함 분석
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            상세 정보 딕셔너리 리스트
        """
        tokens = self.analyze(text)
        
        result = []
        for token in tokens:
            result.append({
                '형태소': token.form,
                '품사': token.tag,
                '품사설명': self.POS_TAGS.get(token.tag, '기타'),
                '점수': round(token.score, 4),
                '확률': round(token.probability, 6),
                '시작위치': token.start,
                '길이': token.length,
                '태그형태': token.tagged_form
            })
        
        return result
    
    def analyze_with_confidence(
        self, 
        text: str, 
        confidence_threshold: float = -10.0,
        show_details: bool = True
    ) -> Dict:
        """
        신뢰도 기반 분석 (통합 버전)
        
        Args:
            text: 분석할 텍스트
            confidence_threshold: 신뢰도 임계값
            show_details: 상세 정보 표시 여부
            
        Returns:
            분석 결과 딕셔너리
        """
        tokens = self.analyze(text)
        
        # 신뢰도 높은 토큰 필터링
        confident_tokens = [
            token for token in tokens
            if token.score > confidence_threshold 
            and token.tag in self.MEANINGFUL_TAGS
        ]
        
        result = {
            '원본': text,
            '전체토큰수': len(tokens),
            '키워드수': len(confident_tokens),
            '키워드': [t.form for t in confident_tokens],
            '명사': [t.form for t in confident_tokens if t.tag in ['NNG', 'NNP']],
            '동사': [t.form for t in confident_tokens if t.tag == 'VV'],
            '형용사': [t.form for t in confident_tokens if t.tag == 'VA'],
        }
        
        if show_details:
            result['상세정보'] = [
                {
                    '형태소': t.form,
                    '품사': t.tag,
                    '점수': round(t.score, 4),
                    '확률': round(t.probability, 6)
                }
                for t in confident_tokens
            ]
        
        return result
    
    def print_analysis(self, text: str, detailed: bool = False):
        """
        분석 결과 예쁘게 출력
        
        Args:
            text: 분석할 텍스트
            detailed: 상세 정보 출력 여부
        """
        print("=" * 60)
        print(f"📝 원본: {text}")
        print("=" * 60)
        
        tokens = self.analyze(text)
        
        if detailed:
            print(f"\n{'번호':<4} {'형태소':<15} {'품사':<6} {'품사설명':<12} {'점수':<10} {'확률':<10}")
            print("-" * 70)
            for i, token in enumerate(tokens):
                pos_desc = self.POS_TAGS.get(token.tag, '기타')
                print(f"[{i+1:2d}] {token.form:<15s} {token.tag:<6s} {pos_desc:<12s} "
                      f"{token.score:>8.4f} {token.probability:>8.6f}")
        else:
            print(f"\n{'번호':<4} {'형태소':<15} {'품사':<8} {'점수':<12}")
            print("-" * 50)
            for i, token in enumerate(tokens):
                print(f"[{i+1:2d}] {token.form:<15s} {token.tag:<8s} {token.score:>10.4f}")
        
        # 요약 정보
        nouns = [t.form for t in tokens if t.tag in ['NNG', 'NNP']]
        verbs = [t.form for t in tokens if t.tag == 'VV']
        
        print(f"\n💡 요약:")
        print(f"  - 총 토큰: {len(tokens)}개")
        print(f"  - 명사: {nouns}")
        print(f"  - 동사: {verbs}")


# ========================================
# 🎯 사용 예제 모음
# ========================================

def example_basic():
    """기본 사용 예제"""
    print("=" * 60)
    print("🚀 예제 1: 기본 형태소 분석")
    print("=" * 60)
    
    analyzer = KoreanMorphologicalAnalyzer()
    
    text = "안녕하세요, Kiwi 토크나이저를 사용해보겠습니다."
    analyzer.print_analysis(text, detailed=True)


def example_keyword_extraction():
    """키워드 추출 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 2: 신뢰도 기반 키워드 추출")
    print("=" * 60)
    
    analyzer = KoreanMorphologicalAnalyzer()
    
    texts = [
        "Python은 AI 개발에 적합한 언어입니다.",
        "LangChain과 Kiwi를 활용한 검색 시스템",
        "형태소 분석은 자연어 처리의 기초입니다."
    ]
    
    for text in texts:
        keywords = analyzer.extract_keywords(text, confidence_threshold=-10.0)
        print(f"\n📝 원본: {text}")
        print(f"✅ 키워드: {keywords}")


def example_pos_extraction():
    """품사별 추출 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 3: 품사별 토큰 추출")
    print("=" * 60)
    
    analyzer = KoreanMorphologicalAnalyzer()
    
    text = "LangChain은 대화형 AI 애플리케이션을 구축하기 위한 프레임워크입니다."
    
    print(f"📝 원본: {text}\n")
    print(f"📌 명사: {analyzer.extract_nouns(text)}")
    print(f"📌 동사: {analyzer.extract_verbs(text)}")
    print(f"📌 형용사: {analyzer.extract_adjectives(text)}")


def example_detailed_analysis():
    """상세 분석 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 4: 상세 분석")
    print("=" * 60)
    
    analyzer = KoreanMorphologicalAnalyzer()
    
    text = "RAG 시스템을 쉽게 만들 수 있어요."
    
    result = analyzer.analyze_with_confidence(text, confidence_threshold=-10.0)
    
    print(f"📝 원본: {result['원본']}")
    print(f"📊 전체 토큰: {result['전체토큰수']}개")
    print(f"📊 키워드: {result['키워드수']}개")
    print(f"\n💡 추출된 정보:")
    print(f"  - 키워드: {result['키워드']}")
    print(f"  - 명사: {result['명사']}")
    print(f"  - 동사: {result['동사']}")
    
    if '상세정보' in result:
        print(f"\n🔍 상세 정보:")
        for info in result['상세정보']:
            print(f"  - {info['형태소']:<10s} | {info['품사']:<6s} | "
                f"점수: {info['점수']:>8.4f} | 확률: {info['확률']:.6f}")


def example_batch_processing():
    """배치 처리 예제"""
    print("\n" + "=" * 60)
    print("🚀 예제 5: 배치 텍스트 처리")
    print("=" * 60)
    
    analyzer = KoreanMorphologicalAnalyzer()
    
    documents = [
        "Python은 데이터 과학에 널리 사용됩니다.",
        "AI 기술이 빠르게 발전하고 있습니다.",
        "자연어 처리는 매우 중요한 분야입니다."
    ]
    
    print("📚 문서별 키워드 추출:\n")
    for i, doc in enumerate(documents):
        keywords = analyzer.extract_keywords(doc, confidence_threshold=-8.0)
        print(f"[{i+1}] {doc}")
        print(f"    → 키워드: {keywords}\n")


# ========================================
# 🎬 메인 실행
# ========================================

if __name__ == "__main__":
    # 모든 예제 실행
    example_basic()
    example_keyword_extraction()
    example_pos_extraction()
    example_detailed_analysis()
    example_batch_processing()
    
    print("\n" + "=" * 60)
    print("✅ 모든 예제 완료!")
    print("=" * 60)