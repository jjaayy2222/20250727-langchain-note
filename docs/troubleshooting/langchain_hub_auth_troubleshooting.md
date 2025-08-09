# 🛠️ LangChain Hub / LangSmith Troubleshooting 기록

> 작성일: 2025-08-10  
> 작성자: Jay  
---

## 1. username 관련 문제

### 1) 원인  
- LangChain Hub가 기존 username 기반 계정 체계에서  
- 조직(organization) 단위 UUID 기반 계정 체계로 전환됨  
- 허브 웹 UI, CLI, API에서 username 노출이나 접근이 제한적임

### 2) 증상  
- 웹 프로필이나 username 메뉴가 보이지 않음  
- `hub.push()` 시 username을 모르거나 사용할 수 없어 업로드 실패  
- CLI 인증 명령어가 작동하지 않음  
- API 키는 있지만 username 없이 호출이 어려움

### 3) 임시 대응  
- 환경변수 `LANGCHAIN_ORGANIZATION`에 조직 UUID를 넣고 시도  
- `hub.push()` 시 username 대신 UUID 사용 시도  
- 그래도 안 되면 `@traceable` 데코레이터 방식으로 실행 추적 전환 권장

---

## 2. Hub 웹 UI 및 CLI 기능 불일치

### 1) 원인  
- LangChain Hub 웹 UI는 Playground 중심으로 재편됨  
- 저장소 관리 기능(생성, 수정, 삭제 등)이 숨겨지거나 제거됨  
- CLI/API와 웹 UI 간 동기화가 완전하지 않음

### 2) 증상  
- 저장소 만들기 기능 웹에서 안 보임  
- CLI 로그인/인증 명령어 동작 안 함  
- 허브에서 프롬프트 업로드/관리 불편

### 3) 임시 대응  
- 로컬에서 프롬프트 직접 관리  
- LangSmith 추적 기능(`@traceable`) 활용  
- 공식 문서, GitHub 이슈, 커뮤니티 업데이트 주시

---

## 3. 환경변수 및 인증 오류

### 1) 원인  
- API 키, 조직 UUID 등 환경변수가 정확히 설정되어야 함  
- 인증 토큰(API 키) 전달 누락 시 호출 실패  
- `hub.push()` 함수에 API 키 명시 전달 권장

### 2) 증상  
- 인증 관련 오류 메시지 발생  
- 프롬프트 업로드 실패

### 3) 해결법  
- `.env` 파일 재확인 및 커널 재시작  
- `LANGCHAIN_API_KEY`, `LANGSMITH_API_KEY` 둘 중 하나라도 설정  
- 코드 내 API 키 직접 전달

---

## 4. 대안: `@traceable` 데코레이터 활용

### 1) 장점  
- 로컬 함수 실행 시점에서 프롬프트와 결과를 자동 기록  
- 허브 업로드 대신 실행 기록 기반 추적 가능  
- username 문제, 저장소 생성 문제 우회 가능

### 2) 사용법 간략 예제

```python
from langsmith import traceable

@traceable
def run_chain(context: str):
    # 프롬프트, LLM 체인 실행 코드
    ...
    return result
````

---

## 5. 참고 링크 및 커뮤니티

* LangChain GitHub 이슈: [https://github.com/hwchase17/langchain/issues](https://github.com/hwchase17/langchain/issues)
* LangChain Discord: [https://discord.gg/langchain](https://discord.gg/langchain)
* LangSmith 공식 문서: [https://docs.langchain.com/langsmith/](https://docs.langchain.com/langsmith/)


