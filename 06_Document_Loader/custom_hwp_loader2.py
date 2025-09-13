# 06_Document_Loader/custom_hwp_loader.py - 한컴 공식 방법 적용
import os
import olefile
import zlib
import struct
from typing import Iterator, List
from langchain_core.documents import Document
from langchain_core.document_loaders.base import BaseLoader

class CustomHWPLoader(BaseLoader):
    """한컴 공식 방법 기반 HWP 로더"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def lazy_load(self) -> Iterator[Document]:
        """HWP 파일을 로드하여 Document로 변환"""
        try:
            text_content = self._extract_hwp_text()
            
            metadata = {
                "source": self.file_path,
                "file_type": "hwp",
                "extraction_method": "hancom_official"
            }
            
            yield Document(
                page_content=text_content,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"HWP 로딩 오류: {e}")
            yield Document(
                page_content=f"HWP 파일 로딩 실패: {e}",
                metadata={"source": self.file_path, "error": str(e)}
            )
    
    def _extract_hwp_text(self) -> str:
        """한컴 공식 방법으로 HWP 텍스트 추출"""
        try:
            f = olefile.OleFileIO(self.file_path)
            dirs = f.listdir()
            
            print(f"📁 HWP 내부 구조:")
            for d in dirs:
                print(f"  - {'/'.join(d) if isinstance(d, list) else d}")
            
            # HWP 파일 검증
            if ["FileHeader"] not in dirs or ["\\x05HwpSummaryInformation"] not in dirs:
                print("⚠️  HWP 파일 형식이 아닙니다")
                return self._try_prvtext_method(f)
            
            # 문서 포맷 압축 여부 확인
            header = f.openstream("FileHeader")
            header_data = header.read()
            is_compressed = (header_data & 1) == 1
            print(f"🗜️  압축 여부: {is_compressed}")
            
            # Body Sections 찾기
            nums = []
            for d in dirs:
                if isinstance(d, list) and len(d) >= 2 and d == "BodyText":
                    try:
                        section_num = int(d[21][len("Section"):])
                        nums.append(section_num)
                    except:
                        continue
            
            if not nums:
                print("📄 BodyText 섹션을 찾을 수 없음, PrvText 방법 시도")
                return self._try_prvtext_method(f)
                
            sections = [f"BodyText/Section{x}" for x in sorted(nums)]
            print(f"📑 발견된 섹션: {sections}")
            
            # 전체 텍스트 추출
            text = ""
            for section in sections:
                try:
                    print(f"🔍 섹션 처리 중: {section}")
                    bodytext = f.openstream(section)
                    data = bodytext.read()
                    
                    if is_compressed:
                        unpacked_data = zlib.decompress(data, -15)
                    else:
                        unpacked_data = data
                    
                    # 각 섹션 내 텍스트 추출
                    section_text = self._extract_section_text(unpacked_data)
                    text += section_text + "\n"
                    
                except Exception as e:
                    print(f"❌ 섹션 {section} 처리 오류: {e}")
                    continue
            
            return text if text.strip() else self._try_prvtext_method(f)
            
        except Exception as e:
            print(f"❌ HWP 추출 오류: {e}")
            return f"HWP 추출 실패: {e}"
        finally:
            if 'f' in locals():
                f.close()
    
    def _extract_section_text(self, unpacked_data: bytes) -> str:
        """섹션 데이터에서 텍스트 추출"""
        section_text = ""
        i = 0
        size = len(unpacked_data)
        
        try:
            while i < size:
                if i + 4 > size:
                    break
                    
                header = struct.unpack_from("<I", unpacked_data, i)
                rec_type = header & 0x3ff
                rec_len = (header >> 20) & 0xfff
                
                # 텍스트 레코드 타입 (67번)
                #if rec_type in :
                if rec_type == 67:
                    if i + 4 + rec_len <= size:
                        rec_data = unpacked_data[i + 4:i + 4 + rec_len]
                        try:
                            text = rec_data.decode('utf-16le')
                            section_text += text + "\n"
                        except:
                            try:
                                text = rec_data.decode('utf-16')
                                section_text += text + "\n"
                            except:
                                pass
                
                i += 4 + rec_len
                
        except Exception as e:
            print(f"⚠️  섹션 텍스트 추출 중 오류: {e}")
        
        return section_text
    
    def _try_prvtext_method(self, f) -> str:
        """PrvText 방법으로 텍스트 추출 (백업 방법)"""
        try:
            print("🔄 PrvText 방법으로 시도 중...")
            encoded_text = f.openstream('PrvText').read()
            decoded_text = encoded_text.decode('UTF-16le')
            print("✅ PrvText 방법 성공!")
            return decoded_text
        except Exception as e:
            print(f"❌ PrvText 방법도 실패: {e}")
            return f"모든 추출 방법 실패: PrvText 오류 - {e}"

'''
if __name__ == "__main__":
    import os
    
    # 현재 파일의 디렉토리 기준으로 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hwp_file_path = os.path.join(current_dir, "data", "디지털 정부혁신 추진계획.hwp")
    
    print(f"📁 파일 경로: {hwp_file_path}")
    print(f"✅ 파일 존재 여부: {os.path.exists(hwp_file_path)}")
    
    if os.path.exists(hwp_file_path):
        print("\n🚀 HWP 파싱 시작...")
        loader = CustomHWPLoader(hwp_file_path)
        docs = loader.load()
        
        print(f"\n🎉 성공! 로드된 문서: {len(docs)}")
        print(f"📄 내용 길이: {len(docs[2].page_content)} 문자")
        print(f"\n📋 내용 미리보기:")
        print("=" * 60)
        print(docs[2].page_content[:2000])  # 2000자까지 출력
        print("=" * 60)
        print(f"\n📊 메타데이터: {docs[2].metadata}")
    else:
        print("❌ 파일을 찾을 수 없습니다!")
'''

# custom_hwp_loader2.py 맨 아래 부분만 수정
if __name__ == "__main__":
    import os
    
    # 현재 파일의 디렉토리 기준으로 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hwp_file_path = os.path.join(current_dir, "data", "디지털 정부혁신 추진계획.hwp")
    
    print(f"📁 파일 경로: {hwp_file_path}")
    print(f"✅ 파일 존재 여부: {os.path.exists(hwp_file_path)}")
    
    if os.path.exists(hwp_file_path):
        print("\n🚀 HWP 파싱 시작...")
        loader = CustomHWPLoader(hwp_file_path)
        docs = loader.load()  # 이건 리스트를 반환함
        
        print(f"\n🎉 성공! 로드된 문서: {len(docs)}")
        
        if docs:  # 문서가 존재하는지 확인
            first_doc = docs[0]  # 첫 번째 문서 가져오기
            print(f"📄 내용 길이: {len(first_doc.page_content)} 문자")
            print(f"\n📋 내용 미리보기:")
            print("=" * 60)
            print(first_doc.page_content[:2000])  # 2000자까지 출력
            print("=" * 60)
            print(f"\n📊 메타데이터: {first_doc.metadata}")
        else:
            print("❌ 문서를 로드할 수 없었습니다!")
    else:
        print("❌ 파일을 찾을 수 없습니다!")