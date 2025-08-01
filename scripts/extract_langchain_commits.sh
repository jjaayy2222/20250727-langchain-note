#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# ✅ langchain 프로젝트 커밋 로그를 Markdown으로 추출해 docs/changelog 폴더에 저장
# 저장 위치는 항상 프로젝트 경로의 docs/changelog 폴더로 고정됨

output_path="/Users/jay/Projects/20250727-langchain-note/docs/changelog/langchain-commit-message-from-git.md"

{
  echo "# 🧾 커밋 메시지 스냅샷 (with 날짜/시간)"
  echo ""

  git log --pretty=format:"- %ad → %s%n%n%b" --date=format:"%Y-%m-%d %H:%M:%S" \
  | sed 's/\\n/\
/g'
} > "$output_path"

echo "✅ 커밋 메시지 로그 저장 완료: $output_path"

# ✅ langchain 프로젝트 커밋 로그를 Markdown으로 추출해 docs/changelog 폴더에 저장