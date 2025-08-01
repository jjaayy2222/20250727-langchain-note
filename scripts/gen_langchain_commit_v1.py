#!/usr/bin/env python3
import subprocess
import re

def get_recent_prefix(default="13.0"):
    try:
        log_output = subprocess.check_output(
            ["git", "log", "-n", "10", "--pretty=%s"],
            universal_newlines=True
        )
        match = re.findall(r"#([\d\.]+)", log_output)
        return match[0] if match else default
    except:
        return default

def prompt_multiline(prefix="📝 본문 (여러 줄 가능, 빈 줄로 종료):"):
    print(prefix)
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    commit_types = ["feat", "fix", "docs", "chore", "refactor", "build"]

    print("🧩 커밋 타입 선택:")
    for idx, ctype in enumerate(commit_types, start=1):
        print(f"{idx}) {ctype}")

    while True:
        try:
            type_choice = int(input("👉 번호 선택: "))
            commit_type = commit_types[type_choice - 1]
            break
        except:
            print("❌ 올바른 번호를 선택해주세요.")

    recent_prefix = get_recent_prefix()
    prefix_input = input(f"🔢 prefix 번호 (Enter = {recent_prefix}): ").strip()
    prefix = prefix_input if prefix_input else recent_prefix

    title = input("📌 커밋 제목: ").strip()
    body = prompt_multiline()

    commit_message = f"{commit_type}[#{prefix}]: {title}"
    if body:
        commit_message += f"\n\n{body}"

    print("\n🧾 최종 커밋 메시지:")
    print("─" * 40)
    print(commit_message)
    print("─" * 40)

    confirm = input("✅ 이 메시지로 git add + commit 하시겠어요? (y/n): ").lower()
    if confirm == "y":
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("🚀 깃 커밋 성공 완료!")
        except subprocess.CalledProcessError:
            print("❌ 깃 커밋 실행 중 오류 발생!")
    else:
        print("⏹ 커밋 취소됨.")

if __name__ == "__main__":
    main()
