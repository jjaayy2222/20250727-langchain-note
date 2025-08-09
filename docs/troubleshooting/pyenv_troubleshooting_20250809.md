# 🛠️ LangChain 프로젝트 트러블슈팅 가이드
> 작성일: 2025-08-98  
> 작성자: Jay  
---

## pyenv 가상환경 관련 이슈

### 문제: ModuleNotFoundError가 계속 발생
- `pip install claude-api-py` 성공했지만 `from claude_api import Client` 실패
- `ModuleNotFoundError`: `No module named 'claude_api'` 지속 발생

**증상**: `pip`으로 설치 → `impor`t에서 실패

**원인**: `python` 명령어가 `가상환경 Python`을 **참조하지 않음**

**해결책**: 
1. `pyenv which python` 확인
2. `PYENV_VERSION` 환경변수와 `.python-version` 파일 일치 확인
3. `pyenv rehash` 실행

### 문제: 환경변수 충돌
**원인**: `PYENV_VERSION`과 `.python-version 파일`이 다른 환경 지정

**해결책**: `unset PYENV_VERSION` 후 로컬 설정 활용
- `unset PYENV_VERSION` - 환경변수 충돌 해결
- `pip cache purge` - 손상된 캐시 제거

## 패키지 설치 관련 이슈

### 문제: `claude-api-py` 설치 후 `import 실패`  

**증상**: `Successfully installed` 메시지는 나오지만 실제 사용 불가

**해결책**: `unofficial-claude-api` 또는 **`공식 anthropic SDK`** 사용
- `pip uninstall claude-api-py` - 문제 패키지 제거
- `pip install unofficial-claude-api` - 작동하는 대안 사용하려했으나 소용 없었음
- **`공식 anthropic SDK`** 사용해야 함!!!

### 교훈
- `pyenv 환경`에서는 `환경변수`와 `로컬 설정 일치 확인 필수`
- 패키지 설치 성공 != 실제 사용 가능 
- 비공식 패키지보다 **`공식 SDK 사용`** 권장

### 참고
- 날짜: 2025-08-09
- 환경: macOS, pyenv, Python 3.13.5, 해당_env 가상환경
- 소요시간: 약 1시간 (피할 수 있었던 삽질...)
