네, 07번 파일의 마크다운 형식을 확인하고 수정해드리겠습니다. 내용은 동일하게 유지하면서 형식만 정리하겠습니다.

# 📘 07. 코드 프롬프팅 (Code Prompting)

## 핵심 요약
- **코드 작성 프롬프팅**은 개발자의 코딩 속도를 향상시키고 반복 작업을 자동화하는 강력한 도구
- **코드 설명 프롬프팅**은 다른 개발자의 코드를 이해하거나 복잡한 로직을 문서화할 때 유용
- **코드 번역 프롬프팅**은 한 프로그래밍 언어에서 다른 언어로 코드를 변환하여 재사용성을 높임
- **디버깅 및 리뷰 프롬프팅**은 코드의 오류를 찾고 개선점을 제안하여 코드 품질을 향상시킴
- **낮은 Temperature (0.1-0.3)** 설정이 코드 생성에서 정확성과 일관성을 보장하는 데 중요

## 주요 개념과 설명

### 💻 **코드 작성 프롬프팅 (Code Writing Prompts)**
- **목적**: 특정 작업을 수행하는 코드를 자동으로 생성
- **장점**: 개발 시간 단축, 반복 작업 자동화, 보일러플레이트 코드 생성
- **적용 분야**: 스크립트 작성, 함수 구현, 알고리즘 구현, 데이터 처리 코드
- **주의사항**: 생성된 코드는 반드시 검토 및 테스트 필요

### 📖 **코드 설명 프롬프팅 (Code Explanation Prompts)**
- **목적**: 기존 코드의 동작 원리와 구조를 이해하기 쉽게 설명
- **활용**: 코드 리뷰, 문서화, 학습, 유지보수
- **특징**: 단계별 분석, 함수별 설명, 알고리즘 로직 해석

### 🔄 **코드 번역 프롬프팅 (Code Translation Prompts)**
- **목적**: 한 프로그래밍 언어로 작성된 코드를 다른 언어로 변환
- **활용**: 레거시 시스템 마이그레이션, 다중 플랫폼 지원, 프로토타이핑
- **주의점**: 언어별 특성과 라이브러리 차이 고려 필요

### 🐛 **디버깅 및 리뷰 프롬프팅 (Debugging & Review Prompts)**
- **목적**: 코드의 오류 발견, 성능 개선점 제안, 코드 품질 향상
- **기능**: 오류 원인 분석, 수정 방법 제시, 최적화 제안, 보안 취약점 검토

## 프롬프트 예시

### 코드 작성 - Bash 스크립트
```plaintext
# 작업 설명
폴더 내 모든 파일의 이름을 변경하는 Bash 스크립트를 작성해주세요.

요구사항:
- 사용자로부터 폴더명 입력받기
- 각 파일 이름 앞에 "draft_" 접두어 추가
- 폴더 존재 여부 확인
- 오류 처리 포함

Bash 코드:
```

**출력**:
```bash
#!/bin/bash

# 폴더명 입력받기
echo "Enter the folder name: "
read folder_name

# 폴더 존재 여부 확인
if [ ! -d "$folder_name" ]; then
    echo "Folder does not exist."
    exit 1
fi

# 폴더 내 파일들 가져오기
files=( "$folder_name"/* )

# 각 파일 이름 변경
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        new_file_name="$folder_name/draft_$(basename "$file")"
        mv "$file" "$new_file_name"
        echo "Renamed: $(basename "$file") → draft_$(basename "$file")"
    fi
done

echo "Files renamed successfully."
```

### 코드 설명 - Python 함수 분석
```plaintext
# 코드 설명 요청
다음 Python 코드가 어떤 작업을 수행하는지 단계별로 설명해주세요:

import os
import shutil

def organize_files_by_extension(source_folder):
    for filename in os.listdir(source_folder):
        if os.path.isfile(os.path.join(source_folder, filename)):
            file_extension = os.path.splitext(filename)[1:]
            
            if file_extension:
                target_folder = os.path.join(source_folder, file_extension)
                
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                shutil.move(
                    os.path.join(source_folder, filename),
                    os.path.join(target_folder, filename)
                )

설명:
```

**출력**:
이 Python 함수는 **파일 확장자별 자동 정리** 기능을 수행합니다:

**1단계: 폴더 탐색**
- `os.listdir(source_folder)`로 지정된 폴더의 모든 항목을 가져옵니다

**2단계: 파일 필터링** 
- `os.path.isfile()`로 폴더가 아닌 파일만 선별합니다

**3단계: 확장자 추출**
- `os.path.splitext(filename)[1:]`로 파일 확장자를 추출합니다
- 예: "document.pdf" → "pdf"

**4단계: 대상 폴더 생성**
- 확장자명과 동일한 이름의 하위 폴더를 생성합니다
- `os.makedirs()`로 폴더가 없으면 새로 만듭니다

**5단계: 파일 이동**
- `shutil.move()`로 파일을 해당 확장자 폴더로 이동합니다

**결과**: 같은 확장자의 파일들이 각각의 폴더로 자동 분류됩니다

### 코드 번역 - Bash to Python
```plaintext
# 코드 번역 요청
다음 Bash 스크립트를 Python으로 번역해주세요:

#!/bin/bash
echo "Enter the folder name: "
read folder_name

if [ ! -d "$folder_name" ]; then
    echo "Folder does not exist."
    exit 1
fi

files=( "$folder_name"/* )
for file in "${files[@]}"; do
    new_file_name="draft_$(basename "$file")"
    mv "$file" "$new_file_name"
done
echo "Files renamed successfully."

Python 코드:
```

**출력**:
```python
import os
import shutil

def rename_files_with_prefix():
    # 폴더명 입력받기
    folder_name = input("Enter the folder name: ")
    
    # 폴더 존재 여부 확인
    if not os.path.isdir(folder_name):
        print("Folder does not exist.")
        return
    
    # 폴더 내 파일 목록 가져오기
    try:
        files = os.listdir(folder_name)
        
        # 각 파일 이름 변경
        for file in files:
            old_path = os.path.join(folder_name, file)
            
            # 파일인지 확인 (폴더 제외)
            if os.path.isfile(old_path):
                new_filename = f"draft_{file}"
                new_path = os.path.join(folder_name, new_filename)
                
                shutil.move(old_path, new_path)
                print(f"Renamed: {file} → {new_filename}")
        
        print("Files renamed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# 함수 실행
if __name__ == "__main__":
    rename_files_with_prefix()
```

### 디버깅 - 오류 수정
```plaintext
# 디버깅 요청
다음 Python 코드에서 오류가 발생합니다. 문제점을 찾고 수정된 코드를 제공해주세요:

오류 메시지:
NameError: name 'toUpperCase' is not defined

문제 코드:
import os
import shutil

folder_name = input("Enter the folder name: ")
prefix = input("Enter the prefix: ")
text = toUpperCase(prefix)  # 오류 발생 지점

if not os.path.isdir(folder_name):
    print("Folder does not exist.")
    exit(1)

files = os.listdir(folder_name)
for file in files:
    new_filename = f"{text}_{file}"
    shutil.move(
        os.path.join(folder_name, file), 
        os.path.join(folder_name, new_file_name)  # 변수명 불일치
    )

분석 및 수정:
```

**출력**:
## 🐛 문제점 분석

**1. 함수명 오류**: `toUpperCase()`는 존재하지 않는 함수입니다
- **해결**: Python의 내장 메서드 `upper()` 사용

**2. 변수명 불일치**: `new_filename`으로 정의했으나 `new_file_name`으로 사용
- **해결**: 변수명 통일

## ✅ 수정된 코드

```python
import os
import shutil

def rename_files_with_prefix():
    folder_name = input("Enter the folder name: ")
    prefix = input("Enter the prefix: ")
    
    # 올바른 대문자 변환 메서드 사용
    text = prefix.upper()
    
    if not os.path.isdir(folder_name):
        print("Folder does not exist.")
        return
    
    try:
        files = os.listdir(folder_name)
        
        for file in files:
            if os.path.isfile(os.path.join(folder_name, file)):
                # 변수명 통일
                new_filename = f"{text}_{file}"
                
                old_path = os.path.join(folder_name, file)
                new_path = os.path.join(folder_name, new_filename)
                
                shutil.move(old_path, new_path)
                print(f"Renamed: {file} → {new_filename}")
        
        print("Files renamed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    rename_files_with_prefix()
```

## 💡 추가 개선 사항

1. **오류 처리 강화**: try-except 블록 추가
2. **파일 필터링**: 디렉터리 제외하고 파일만 처리
3. **함수화**: 재사용 가능한 함수로 구조화
4. **사용자 피드백**: 각 파일 처리 상황 출력

## 활용 팁

### 🚀 **LangChain에서의 코드 생성 체인**
```python
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.chains import LLMChain

# 코드 생성 프롬프트 템플릿
code_generation_template = """
작업: {task}
프로그래밍 언어: {language}
요구사항:
{requirements}

다음 형식으로 코드를 작성해주세요:
1. 코드 설명 (주석 포함)
2. 완전한 실행 가능한 코드
3. 사용 예시

코드:
"""

code_prompt = PromptTemplate(
    input_variables=["task", "language", "requirements"],
    template=code_generation_template
)

# 낮은 temperature로 정확한 코드 생성
llm = VertexAI(
    model_name="gemini-pro",
    temperature=0.1,  # 코드 생성시 정확성 우선
    max_output_tokens=2048
)

code_chain = LLMChain(llm=llm, prompt=code_prompt)

# 사용 예시
result = code_chain.run(
    task="CSV 파일을 읽어서 데이터 분석하는 스크립트",
    language="Python",
    requirements="""
    - pandas 라이브러리 사용
    - 기본 통계 정보 출력
    - 시각화 포함 (matplotlib)
    - 오류 처리 포함
    """
)
```

### 🔧 **코드 리뷰 자동화 체인**
```python
class CodeReviewChain:
    def __init__(self, llm):
        self.llm = llm
        self.review_template = """
다음 {language} 코드를 리뷰하고 개선점을 제안해주세요:

```
{code}
```

다음 관점에서 분석해주세요:
1. 코드 품질 및 가독성
2. 성능 최적화 가능성
3. 보안 취약점
4. 오류 처리
5. 코딩 컨벤션 준수

리뷰 결과:
- 전체 평가: [1-10점]
- 주요 문제점: 
- 개선 제안:
- 수정된 코드 (필요시):
"""
    
    def review_code(self, code: str, language: str = "python") -> str:
        """코드 리뷰 수행"""
        prompt = self.review_template.format(
            code=code,
            language=language
        )
        
        response = self.llm.predict(prompt)
        return response
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """코드 설명 생성"""
        explain_prompt = f"""
다음 {language} 코드의 동작을 초보자도 이해할 수 있게 단계별로 설명해주세요:

```
{code}
```

설명:
1. 전체 목적:
2. 주요 구성 요소:
3. 단계별 동작:
4. 사용된 기술/라이브러리:
"""
        
        return self.llm.predict(explain_prompt)

# 사용 예시
llm = VertexAI(model_name="gemini-pro", temperature=0.2)
reviewer = CodeReviewChain(llm)

sample_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""

review_result = reviewer.review_code(sample_code, "python")
explanation = reviewer.explain_code(sample_code, "python")
```

### 🎯 **다중 언어 코드 번역기**
```python
class CodeTranslator:
    def __init__(self, llm):
        self.llm = llm
        
    def translate_code(self, source_code: str, from_lang: str, to_lang: str, 
                      include_comments: bool = True) -> str:
        """코드를 다른 언어로 번역"""
        
        comment_instruction = "주석과 설명도 함께 포함해주세요." if include_comments else ""
        
        translate_prompt = f"""
다음 {from_lang} 코드를 {to_lang}으로 번역해주세요.

원본 코드:
```
{source_code}
```

번역 요구사항:
- 동일한 기능 구현
- {to_lang}의 관례와 베스트 프랙티스 적용
- 필요한 라이브러리 import 포함
{comment_instruction}

번역된 {to_lang} 코드:
"""
        
        return self.llm.predict(translate_prompt)
    
    def batch_translate(self, code_snippets: list, from_lang: str, to_lang: str) -> list:
        """여러 코드 스니펫 일괄 번역"""
        results = []
        
        for i, code in enumerate(code_snippets):
            print(f"번역 중... ({i+1}/{len(code_snippets)})")
            translated = self.translate_code(code, from_lang, to_lang)
            results.append({
                'original': code,
                'translated': translated,
                'from': from_lang,
                'to': to_lang
            })
        
        return results

# 사용 예시
translator = CodeTranslator(llm)

bash_script = """
#!/bin/bash
for file in *.txt; do
    echo "Processing $file"
    wc -l "$file"
done
"""

python_version = translator.translate_code(bash_script, "bash", "python")
print(python_version)
```

### 🐛 **스마트 디버거**
```python
class SmartDebugger:
    def __init__(self, llm):
        self.llm = llm
    
    def debug_error(self, code: str, error_message: str, language: str = "python") -> dict:
        """오류 메시지를 기반으로 코드 디버깅"""
        
        debug_prompt = f"""
다음 {language} 코드에서 오류가 발생했습니다:

오류 메시지:
```
{error_message}
```

코드:
```
{code}
```

다음을 분석해주세요:
1. 오류 원인 분석
2. 구체적인 수정 방법
3. 수정된 코드
4. 예방 방법
5. 관련 베스트 프랙티스

분석 결과:
"""
        
        response = self.llm.predict(debug_prompt)
        
        # 구조화된 결과 반환
        return {
            'original_code': code,
            'error_message': error_message,
            'analysis': response,
            'language': language
        }
    
    def optimize_code(self, code: str, language: str = "python") -> str:
        """코드 성능 최적화 제안"""
        
        optimize_prompt = f"""
다음 {language} 코드의 성능을 개선할 수 있는 방법을 제안해주세요:

```
{code}
```

분석할 영역:
- 시간 복잡도 개선
- 메모리 사용량 최적화
- 가독성 향상
- 에러 처리 강화

최적화 제안:
"""
        
        return self.llm.predict(optimize_prompt)
    
    def security_audit(self, code: str, language: str = "python") -> str:
        """보안 취약점 검사"""
        
        security_prompt = f"""
다음 {language} 코드의 보안 취약점을 검사해주세요:

```
{code}
```

검사 항목:
- 입력 검증
- SQL 인젝션 가능성
- XSS 취약점
- 파일 시스템 접근 보안
- 권한 관리
- 데이터 노출 위험

보안 분석 결과:
"""
        
        return self.llm.predict(security_prompt)

# 사용 예시
debugger = SmartDebugger(llm)

# 오류 코드 예시
buggy_code = """
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
"""

error_msg = "ZeroDivisionError: division by zero"

debug_result = debugger.debug_error(buggy_code, error_msg)
optimization = debugger.optimize_code(buggy_code)
security_audit = debugger.security_audit(buggy_code)
```

### 📊 **코드 품질 메트릭 분석기**
```python
class CodeQualityAnalyzer:
    def __init__(self, llm):
        self.llm = llm
    
    def analyze_quality(self, code: str, language: str = "python") -> dict:
        """종합적인 코드 품질 분석"""
        
        quality_prompt = f"""
다음 {language} 코드의 품질을 종합적으로 분석해주세요:

```
{code}
```

평가 기준 (각 항목을 1-10점으로 평가):
1. 가독성 (Readability)
2. 유지보수성 (Maintainability)  
3. 성능 (Performance)
4. 보안 (Security)
5. 테스트 가능성 (Testability)
6. 재사용성 (Reusability)

JSON 형식으로 결과를 반환해주세요:
```
{{
  "overall_score": 0,
  "scores": {{
    "readability": 0,
    "maintainability": 0,
    "performance": 0,
    "security": 0,
    "testability": 0,
    "reusability": 0
  }},
  "strengths": ["강점1", "강점2"],
  "weaknesses": ["약점1", "약점2"],
  "recommendations": ["개선사항1", "개선사항2"]
}}
```
"""
        
        response = self.llm.predict(quality_prompt)
        
        try:
            import json
            quality_data = json.loads(response.strip())
            return quality_data
        except:
            return {"error": "분석 결과를 파싱할 수 없습니다", "raw_response": response}
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """코드에 대한 테스트 케이스 생성"""
        
        test_prompt = f"""
다음 {language} 코드에 대한 단위 테스트를 작성해주세요:

```
{code}
```

테스트 요구사항:
- 정상 케이스 테스트
- 경계값 테스트  
- 예외 상황 테스트
- {language}의 표준 테스팅 프레임워크 사용

테스트 코드:
"""
        
        return self.llm.predict(test_prompt)

# 사용 예시
analyzer = CodeQualityAnalyzer(llm)

sample_function = """
def calculate_bmi(weight, height):
    if height <= 0:
        raise ValueError("Height must be positive")
    
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return round(bmi, 2), category
"""

quality_report = analyzer.analyze_quality(sample_function)
test_cases = analyzer.generate_tests(sample_function)

print(f"전체 점수: {quality_report.get('overall_score', 'N/A')}/10")
print(f"테스트 코드:\n{test_cases}")
```

### 📝 코드 문서화 자동 생성기

```python
class CodeDocumentationGenerator:
    def __init__(self, llm):
        self.llm = llm
    
    def generate_docstring(self, function_code: str, language: str = "python") -> str:
        """함수에 대한 docstring 생성"""
        
        docstring_prompt = f"""
다음 {language} 함수에 대한 상세한 docstring을 생성해주세요:

```
{function_code}
```

포함할 내용:
- 함수 목적 및 기능 설명
- 매개변수 설명 (타입 포함)
- 반환값 설명 (타입 포함)
- 예외 처리 정보
- 사용 예시
- {language} 표준 docstring 형식 준수

Docstring:
"""
        return self.llm.predict(docstring_prompt)
    
    def generate_readme(self, project_code: str, project_name: str) -> str:
        """프로젝트 README 생성"""
        
        readme_prompt = f"""
다음 코드를 기반으로 프로젝트 "{project_name}"의 README.md 파일을 생성해주세요:

```
{project_code}
```

README에 포함할 내용:
- 프로젝트 개요
- 주요 기능
- 설치 방법
- 사용법 (예시 포함)
- API 문서 (해당하는 경우)
- 기여 방법
- 라이선스 정보

Markdown 형식의 README:
"""
        return self.llm.predict(readme_prompt)

# 사용 예시
doc_generator = CodeDocumentationGenerator(llm)

function_code = """
def merge_sorted_arrays(arr1, arr2):
    result = []
    i, j = 0, 0
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    
    return result
"""

docstring = doc_generator.generate_docstring(function_code)
print(docstring)
```

### 🎯 언어별 최적 설정 가이드

| 언어       | Temperature | Max Tokens | 특별 고려사항             |
|------------|-------------|------------|--------------------------|
| Python     | 0.1-0.2     | 1024-2048  | PEP8 준수, 타입 힌트      |
| JavaScript | 0.1-0.3     | 1024-2048  | ES6+ 문법, 모듈화         |
| Java       | 0.1         | 2048-4096  | 객체지향 원칙, 예외 처리  |
| Bash       | 0.1         | 512-1024   | 오류 처리, 가독성         |
| SQL        | 0.1         | 1024       | 성능 최적화, 보안         |
| HTML/CSS   | 0.2-0.4     | 1024-2048  | 접근성, 반응형 디자인     |

### ⚠️ 코드 프롬프팅 주의사항

```python
class CodePromptingBestPractices:
    """코드 프롬프팅 모범 사례"""

    @staticmethod
    def validate_generated_code(code: str, language: str) -> dict:
        """생성된 코드 검증"""
        warnings = []

        # 기본 검증 항목들
        if "TODO" in code or "FIXME" in code:
            warnings.append("미완성 코드가 포함되어 있습니다")

        if language == "python":
            if "input()" in code and "try:" not in code:
                warnings.append("사용자 입력에 대한 예외 처리가 필요할 수 있습니다")

            if "import os" in code and "path.exists" not in code:
                warnings.append("파일/디렉터리 존재 여부 확인을 고려하세요")

        return {
            "is_safe": len(warnings) == 0,
            "warnings": warnings,
            "recommendations": [
                "생성된 코드를 실행하기 전에 반드시 검토하세요",
                "테스트 환경에서 먼저 확인하세요",
                "보안 취약점을 체크하세요"
            ]
        }

    @staticmethod
    def create_safe_prompt(task: str, language: str) -> str:
        """안전한 코드 생성 프롬프트 작성"""

        safety_instructions = '''
다음 보안 및 품질 기준을 준수해주세요:
- 입력 검증 포함
- 적절한 오류 처리
- 보안 취약점 방지
- 코드 주석 포함
- 테스트 가능한 구조
'''

        return f"""{safety_instructions}

작업: {task}
언어: {language}

요구사항을 충족하는 안전하고 품질 높은 코드를 작성해주세요:
"""

# 사용 예시
best_practices = CodePromptingBestPractices()

# 안전한 프롬프트 생성
safe_prompt = best_practices.create_safe_prompt(
    "파일 업로드 처리 함수",
    "python"
)

# 생성된 코드 검증
sample_code = '''
def upload_file(filename):
    with open(filename, 'r') as f:
        return f.read()
'''

validation = best_practices.validate_generated_code(sample_code, "python")
print(f"안전성 검사: {'통과' if validation['is_safe'] else '주의 필요'}")
if validation['warnings']:
    print("경고사항:", validation['warnings'])
```

### 🔄 지속적 개선 및 학습

```python
from datetime import datetime

class CodePromptLearner:
    def __init__(self):
        self.prompt_history = []
        self.success_patterns = []

    def log_prompt_result(self, prompt: str, generated_code: str,
                         success: bool, feedback: str = ""):
        """프롬프트 결과 로깅"""

        self.prompt_history.append({
            'prompt': prompt,
            'generated_code': generated_code,
            'success': success,
            'feedback': feedback,
            'timestamp': datetime.now()
        })

        if success:
            self.success_patterns.append({
                'prompt_structure': self._analyze_prompt_structure(prompt),
                'code_quality': self._analyze_code_quality(generated_code)
            })

    def get_best_practices_summary(self) -> dict:
        """성공 패턴 분석 요약"""
        if not self.success_patterns:
            return {"message": "충분한 데이터가 없습니다"}

        return {
            "총 시도": len(self.prompt_history),
            "성공률": sum(1 for h in self.prompt_history if h['success']) / len(self.prompt_history),
            "개선 권장사항": self._generate_recommendations()
        }

    def _analyze_prompt_structure(self, prompt: str) -> dict:
        """프롬프트 구조 분석"""
        return {
            "has_examples": "예시" in prompt or "example" in prompt.lower(),
            "has_requirements": "요구사항" in prompt or "requirements" in prompt.lower(),
            "has_constraints": "제약" in prompt or "constraint" in prompt.lower(),
            "length": len(prompt)
        }

    def _analyze_code_quality(self, code: str) -> dict:
        """코드 품질 분석"""
        return {
            "has_comments": "#" in code or "//" in code or "\"\"\"" in code,
            "has_error_handling": "try" in code or "except" in code or "catch" in code,
            "length": len(code),
            "function_count": code.count("def ") + code.count("function ")
        }

    def _generate_recommendations(self) -> list:
        """개선 권장사항 생성"""
        return [
            "구체적인 요구사항을 포함하세요",
            "예시를 제공하면 더 좋은 결과를 얻을 수 있습니다",
            "오류 처리를 명시적으로 요청하세요",
            "코드 주석을 요청하세요"
        ]

# 학습 시스템 사용
learner = CodePromptLearner()

# 프롬프트 결과 기록
learner.log_prompt_result(
    prompt="Python으로 파일을 읽는 함수를 만들어주세요",
    generated_code="def read_file(filename): return open(filename).read()",
    success=False,
    feedback="오류 처리가 없음"
)

# 개선된 프롬프트 결과 기록
learner.log_prompt_result(
    prompt="Python으로 파일을 안전하게 읽는 함수를 만들어주세요. 오류 처리와 주석을 포함해주세요.",
    generated_code=\"\"\"
def read_file(filename):
    '''파일을 안전하게 읽는 함수'''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
\"\"\",
    success=True,
    feedback="완벽한 구현"
)

summary = learner.get_best_practices_summary()
print(summary)
```

---

* 출처
    * [1] [Prompt Engineering from Google](https://www.kaggle.com/whitepaper-prompt-engineering)