# 🛠️ VSCode CLI(code) 명령어 인식 오류 해결 로그

> 작성일: 2025-08-01  
> 작성자: Jay  
> 환경: macOS (Apple Silicon), zsh, pyenv, LangChain 개발 환경 구성 중

---

## ❗️ 문제 요약

터미널에서 VSCode를 `code` 명령어로 실행하려고 할 때 다음과 같은 오류 발생:

```
code --version
# 결과:
zsh: command not found: code
```

**상황상 주요 작업 중이었고**, `code .`, `git commit`에서 VSCode를 에디터로 열려고 계획했으나 CLI 실행 불가로 지연됨.

---

## 🔍 원인 분석

| 원인 항목 | 내용 |
|-----------|------|
| VSCode 설치 경로 | `/Applications/Visual Studio Code.app` 에 없었음 |
| code CLI 링크 | 수동으로 `/usr/local/bin/code`에 연결 시도함 |
| 심볼릭 링크 대상 | `.../app/bin/code` 실행 파일이 존재하지 않아 오류 발생 |
| 실제 설치 위치 | `/Users/jay/Downloads/Visual Studio Code.app` ← Finder > 응용프로그램에 안 보였던 이유 |
| PATH | `/usr/local/bin` 경로는 `zshrc`에 잘 설정되어 있었음 (`source ~/.zshrc` 완료됨) |

---

## 🧪 단계별 시도 및 조치 흐름

1. `ls -l /usr/local/bin/code`  
   → 심볼릭 링크는 존재하였음

2. `.zshrc` 최종 점검  
   - 아래 라인 존재 여부 확인 → ✅ 포함됨  
   ```
   export PATH="/usr/local/bin:$PATH"
   ```

3. VSCode 재설치 검토  
   - App Store 설치가 아니라 직접 다운로드(good)  
   - 그러나 `Downloads/` 폴더에서 압축만 풀고 `/Applications`로 이동하지 않아서 인식 실패

4. 명령어 직접 실행 시도  
   ```
   "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" --version
   ```
   → 오류: no such file or directory

5. Spotlight 및 `find ~/ -name ...` 명령으로 실제 설치 위치 추적 성공:
   ```
   /Users/jay/Downloads/Visual Studio Code.app
   ```

---

## ✅ 최종 해결 방법

| 단계 | 수행 내용 |
|------|-----------|
| 1️⃣ | `/Users/jay/Downloads/Visual Studio Code.app` 를 Finder에서 열기 |
| 2️⃣ | 드래그하여 `/Applications` 폴더로 이동 |
| 3️⃣ | VSCode 재실행 → `⌘ + Shift + P` → "Shell Command: Install 'code' command in PATH" 실행 |
| 4️⃣ | 새 터미널에서 확인 |
```
code --version
code .
```

---

## 🧾 최종 확인 결과

```
$ code --version
1.100.1
91fa95bccb027ece6a968589bb1d662fa9c8e170
arm64
```

✅ VSCode CLI 성공적으로 등록됨  
✅ Git 커밋 메시지 편집기도 VSCode로 설정 완료  
✅ `.zshrc` 및 PATH도 정상 설정

---

## 💬 교훈 및 비고

- `Visual Studio Code.app`는 반드시 `/Applications`로 옮겨야 `code` CLI 정상 작동
- App Store 버전은 `code` 명령이 포함되지 않을 수 있음
- macOS에서 CLI 명령 작동 안 할 경우:
  - `ls -l ...`, `echo $PATH`, `find ~/ -name ...`, `which code` 등을 활용해 추적
- 터미널 shell(`zsh`, `bash`) 환경 이해도 중요
- shell 명령어 등록 후 항상 `source ~/.zshrc` 필요

---

## 📌 사용 환경 정보

| 항목 | 값 |
|------|-----|
| OS | macOS Apple Silicon (zsh) |
| Python | pyenv 관리 가상환경 사용 중 |
| VSCode | zip 설치 후 `/Applications`로 이동 완료 |
| 작업 경로 | `~/Projects/20250727-langchain-note/` |
| CLI 사용 목적 | git commit 에디터, 터미널 기반 실행용 |

---

## ✅ 관련 설정 확인 명령 요약

```plaintext
# .zshrc 경로 열기
code ~/.zshrc

# PATH 환경변수 확인
echo $PATH

# VSCode 코드 경로 확인
ls -l /usr/local/bin/code
```

---

_이 문서는 VSCode CLI 설정 오류를 해결하는 과정 중 발생한 조사, 추적, 조치 과정을 기록한 troubleshooting 로그입니다. 재현/재발 시 빠르게 대응할 수 있도록 이 문서를 참조하세요._
