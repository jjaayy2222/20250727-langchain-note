#!/usr/bin/env python3
import subprocess
import re
import os
import json
from pathlib import Path

commit_types = ["feat", "fix", "docs", "chore", "refactor", "build"]
project_root = Path(__file__).resolve().parent.parent                   # 프로젝트 루트 기준으로 경로 고정
CACHE_PATH = "scripts/gen_commit_cache.json"
#LOG_PATH = "docs/changelog/commit-log.md"                              # commit-log.md 파일과 분리
LOG_PATH = "docs/changelog/commit-message-raw-log.md"                   # 생성될 파일

def get_recent_prefix(default="1.1"):
    try:
        log_output = subprocess.check_output(
            ["git", "log", "-n", "10", "--pretty=%s"], universal_newlines=True
        )
        matches = re.findall(r'#(\d+\.\d+)', log_output)
        if matches:
            last = matches[0]
            parts = last.split('.')
            parts[-1] = str(int(parts[-1]) + 1)  # 마지막 숫자 +1
            return '.'.join(parts)
    except Exception:
        pass
    return default

def get_diff_files():
    try:
        files = subprocess.check_output(
            ["git", "diff", "--name-only"],
            universal_newlines=True
        ).strip().split('\n')
        return [f for f in files if f]
    except Exception: return []

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(data):
    with open(CACHE_PATH, "w") as f:
        json.dump(data, f)

def append_to_log(msg):
    header = f"\n- {msg.splitlines()[0]}"
    body = "\n".join(msg.splitlines()[1:])
    entry = header + ('\n' if body else '') + body + '\n'
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(entry)

def prompt_multiline(prompt):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def main():
    cache = load_cache()

    # 변경 파일 안내
    changed = get_diff_files()
    if changed:
        print("📝 변경된 파일:")
        for c in changed:
            print(f"  · {c}")
        print("-" * 40)

    # 커밋 타입
    print("커밋 타입:")
    for idx, tp in enumerate(commit_types, 1):
        print(f"{idx}) {tp}", end="  ")
    print()

    type_def = cache.get("type", "feat")
    type_input = input(f"번호 선택 (Enter={commit_types.index(type_def)+1}): ")
    commit_type = commit_types[int(type_input)-1] if type_input.strip() else type_def

    # prefix 자동 증가
    prefix_def = get_recent_prefix(default=cache.get("prefix", "1.1"))
    prefix_input = input(f"prefix[#번호] (Enter={prefix_def}): ")
    prefix = prefix_input if prefix_input else prefix_def

    # 제목
    title_def = cache.get("title", "")
    title = input(f"커밋 제목 (Enter={title_def}): ").strip() or title_def

    # 본문
    body = prompt_multiline("커밋 본문 (여러 줄, 빈 줄로 종료):")

    # 메시지 완성
    message = f"{commit_type}[#{prefix}]: {title}"
    if body:
        message += "\n\n" + body

    print("\n🧾 최종 메시지 ↓")
    print("="*40)
    print(message)
    print("="*40)

    confirm = input("🚀 이 메시지로 커밋할까요? (y/n, q=취소): ").lower()
    if confirm == 'y':
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", message])
        append_to_log(message)
        print("✅ 커밋+로그 append 완료!")
    else:
        print("⏹️ 커밋 취소됨.")

    # 캐시 저장
    save_cache({"type": commit_type, "prefix": prefix, "title": title})

if __name__ == "__main__":
    main()
