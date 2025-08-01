#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

echo "🧩 커밋 타입 선택:"
echo "1) feat"
echo "2) fix"
echo "3) docs"
echo "4) chore"
echo "5) refactor"
echo "6) build"
read -p "👉 번호 선택 (예: 1): " type_num

# 타입 매핑
case $type_num in
  1) type="feat" ;;
  2) type="fix" ;;
  3) type="docs" ;;
  4) type="chore" ;;
  5) type="refactor" ;;
  6) type="build" ;;
  *) echo "❌ 유효하지 않은 선택!" && exit 1 ;;
esac

read -p "🔢 prefix[#번호]: " prefix
read -p "📝 커밋 제목: " title

echo "✍️  커밋 본문 작성 (여러 줄 가능, 끝내려면 Enter 2번)"
body=""
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && break
  body="${body}${line}\n"
done

# 커밋 메시지 생성
if [[ -z "$body" ]]; then
  message="${type}[#${prefix}]: ${title}"
else
  message="${type}[#${prefix}]: ${title}\n\n${body}"
fi

# 커밋 수행
echo -e "\n🧾 최종 커밋 메시지:"
echo -e "$message"

read -p "🚀 위 메시지로 커밋하시겠습니까? (y/n): " confirm
if [[ $confirm == "y" || $confirm == "Y" ]]; then
  git add .
  git commit -m "$(echo -e "$message")"
  echo "✅ 커밋 완료!"
else
  echo "❎ 커밋 취소됨."
fi
