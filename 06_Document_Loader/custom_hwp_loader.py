# 06_Document_Loader/custom_hwp_loader.py 완전 수정버전
import os
from typing import Iterator, List
from langchain_core.documents import Document
from langchain_core.document_loaders.base import BaseLoader

class CustomHWPLoader(BaseLoader):
    """개선된 HWP 로더 - Python 3.13 호환"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def lazy_load(self) -> Iterator[Document]:
        """HWP 파일을 로드하여 Document로 변환"""
        try:
            # 방법 1: olefile로 시도
            text_content = self._extract_with_olefile()
            
            if not text_content or "추출 실패" in text_content:
                # 방법 2: zipfile로 시도 (HWP 5.0+는 ZIP 기반)
                text_content = self._extract_with_zipfile()
            
            if not text_content or "추출 실패" in text_content:
                # 방법 3: 바이너리 직접 읽기
                text_content = self._extract_with_binary()
                
            metadata = {
                "source": self.file_path,
                "file_type": "hwp",
                "extraction_method": "custom_parser"
            }
            
            yield Document(
                page_content=text_content,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"전체 HWP 로딩 오류: {e}")
            yield Document(
                page_content=f"HWP 파일 로딩 실패: {e}",
                metadata={"source": self.file_path, "error": str(e)}
            )
    
    def _extract_with_olefile(self) -> str:
        """olefile을 사용한 추출"""
        try:
            import olefile
            
            if not olefile.isOleFile(self.file_path):
                return "olefile: HWP 형식이 아님"
            
            with olefile.OleFileIO(self.file_path) as ole:
                sections = []
                
                # 모든 스트림 탐색
                for stream_name in ole.listdir():
                    stream_path = '/'.join(stream_name)
                    
                    # BodyText 관련 스트림 찾기
                    if 'BodyText' in stream_path or 'bodytext' in stream_path.lower():
                        try:
                            data = ole.open(stream_name).read()
                            
                            # 여러 인코딩 시도
                            for encoding in ['utf-16le', 'utf-16', 'cp949', 'euc-kr', 'utf-8']:
                                try:
                                    text = data.decode(encoding, errors='ignore')
                                    if text and len(text.strip()) > 10:  # 의미있는 텍스트인지 확인
                                        sections.append(f"[{encoding}] {text[:500]}")
                                        break
                                except:
                                    continue
                                    
                        except Exception as e:
                            print(f"스트림 읽기 오류 {stream_path}: {e}")
                            continue
                
                result = '\n'.join(sections) if sections else "olefile: 텍스트 섹션을 찾을 수 없음"
                return result
                
        except ImportError:
            return "olefile 라이브러리가 설치되지 않음"
        except Exception as e:
            return f"olefile 추출 실패: {e}"
    
    def _extract_with_zipfile(self) -> str:
        """zipfile을 사용한 추출 (HWP 5.0+)"""
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            
            with zipfile.ZipFile(self.file_path, 'r') as hwp_zip:
                sections = []
                
                # ZIP 내부 파일 목록 확인
                file_list = hwp_zip.namelist()
                print(f"ZIP 내부 파일들: {file_list}")
                
                # XML 파일들 확인
                for file_name in file_list:
                    if file_name.endswith('.xml') or 'content' in file_name.lower():
                        try:
                            content = hwp_zip.read(file_name)
                            
                            # XML 파싱 시도
                            try:
                                root = ET.fromstring(content)
                                # 텍스트 노드 추출
                                for elem in root.iter():
                                    if elem.text and elem.text.strip():
                                        sections.append(elem.text.strip())
                            except:
                                # XML이 아니면 직접 텍스트 추출
                                for encoding in ['utf-8', 'cp949', 'euc-kr']:
                                    try:
                                        text = content.decode(encoding, errors='ignore')
                                        if text and len(text.strip()) > 10:
                                            sections.append(f"[{file_name}] {text[:300]}")
                                            break
                                    except:
                                        continue
                                        
                        except Exception as e:
                            print(f"ZIP 파일 읽기 오류 {file_name}: {e}")
                            continue
                
                return '\n'.join(sections) if sections else "zipfile: 텍스트를 찾을 수 없음"
                
        except zipfile.BadZipFile:
            return "zipfile: ZIP 형식이 아님"
        except Exception as e:
            return f"zipfile 추출 실패: {e}"
    
    def _extract_with_binary(self) -> str:
        """바이너리 직접 읽기로 텍스트 추출"""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            # 한글 문자열 패턴 찾기
            text_parts = []
            
            # 여러 인코딩으로 시도
            for encoding in ['utf-16le', 'cp949', 'euc-kr', 'utf-8']:
                try:
                    decoded = data.decode(encoding, errors='ignore')
                    
                    # 한글이 포함된 문장 찾기
                    import re
                    korean_sentences = re.findall(r'[가-힣\s]{10,}', decoded)
                    
                    if korean_sentences:
                        text_parts.extend([f"[{encoding}] {sent}" for sent in korean_sentences[:5]])
                        
                except:
                    continue
            
            if text_parts:
                return '\n'.join(text_parts)
            else:
                return f"바이너리 추출: 한글 텍스트를 찾을 수 없음 (파일 크기: {len(data)} bytes)"
                
        except Exception as e:
            return f"바이너리 추출 실패: {e}"

if __name__ == "__main__":
    # 절대 경로로 수정
    import os
    
    # 현재 파일의 디렉토리 기준으로 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hwp_file_path = os.path.join(current_dir, "data", "디지털 정부혁신 추진계획.hwp")
    
    print(f"파일 경로: {hwp_file_path}")
    print(f"파일 존재 여부: {os.path.exists(hwp_file_path)}")
    
    if os.path.exists(hwp_file_path):
        # olefile 설치 확인
        try:
            import olefile
            print("✅ olefile 라이브러리 사용 가능")
        except ImportError:
            print("⚠️  olefile 설치 필요: pip install olefile")
        
        loader = CustomHWPLoader(hwp_file_path)
        docs = loader.load()
        
        print(f"\n🎉 성공! 로드된 문서: {len(docs)}")
        print(f"📄 내용 미리보기:")
        print("-" * 50)
        print(docs[0].page_content[:1500])  # 더 많이 출력
        print("-" * 50)
        print(f"📋 메타데이터: {docs[0].metadata}")
    else:
        print("❌ 파일을 찾을 수 없습니다!")
