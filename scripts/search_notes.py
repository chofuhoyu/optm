"""课件内容检索工具。

用法:
  uv run python scripts/search_notes.py "关键词"          # 搜索所有章节
  uv run python scripts/search_notes.py "KKT" --chapter 7 # 只搜索第7章
  uv run python scripts/search_notes.py "梯度" -C 2       # 显示上下文2行
  uv run python scripts/search_notes.py --toc             # 显示所有章节目录
"""

import os
import re
import sys
import io

# 解决 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NOTES_DIR = "extracted"


def search_all(keyword: str, context: int = 1):
    """在所有章节中搜索关键词"""
    files = sorted(
        [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")],
        key=lambda x: int(re.match(r"(\d+)", x).group(1)) if re.match(r"(\d+)", x) else 99,
    )

    total_hits = 0
    for fname in files:
        filepath = os.path.join(NOTES_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        matches = []
        current_slide = ""
        for i, line in enumerate(lines):
            slide_match = re.match(r"<!-- Slide number: (\d+) -->", line)
            if slide_match:
                current_slide = slide_match.group(1)
            if keyword.lower() in line.lower():
                # 收集上下文
                start = max(0, i - context)
                end = min(len(lines), i + context + 1)
                ctx_lines = []
                for j in range(start, end):
                    prefix = ">" if j == i else " "
                    ctx_lines.append(f"  {prefix} [{j+1:4d}] {lines[j].rstrip()}")
                matches.append({
                    "slide": current_slide,
                    "line": i + 1,
                    "context": "\n".join(ctx_lines),
                })

        if matches:
            chapter = fname.replace(".md", "")
            print(f"\n{'='*60}")
            print(f"  {chapter} — {len(matches)} 处匹配")
            print(f"{'='*60}")
            for m in matches:
                print(f"\n  --- Slide {m['slide']}, 行 {m['line']} ---")
                print(m['context'])
            total_hits += len(matches)

    print(f"\n{'='*60}")
    print(f"  总计: {total_hits} 处匹配")
    print(f"{'='*60}")


def search_chapter(keyword: str, chapter: int, context: int = 1):
    """搜索指定章节"""
    for fname in os.listdir(NOTES_DIR):
        if fname.startswith(f"{chapter}") and fname.endswith(".md"):
            filepath = os.path.join(NOTES_DIR, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 按幻灯片分割
            slides = re.split(r"<!-- Slide number: (\d+) -->", content)
            matches = []
            for i in range(1, len(slides), 2):
                slide_num = slides[i]
                slide_text = slides[i + 1] if i + 1 < len(slides) else ""
                if keyword.lower() in slide_text.lower():
                    lines = slide_text.strip().split("\n")
                    snip = "\n".join(f"    {l}" for l in lines[:context * 2 + 1])
                    matches.append((slide_num, snip))

            print(f"\n  {fname.replace('.md', '')} — {len(matches)} 处匹配")
            for slide_num, snip in matches:
                print(f"\n  --- Slide {slide_num} ---")
                print(snip)


def show_toc():
    """显示所有章节的目录（每章的关键主题列表）"""
    files = sorted(
        [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")],
        key=lambda x: int(re.match(r"(\d+)", x).group(1)) if re.match(r"(\d+)", x) else 99,
    )

    for fname in files:
        filepath = os.path.join(NOTES_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取所有 # 标题行
        titles = re.findall(r"^#+\s*(.+)$", content, re.MULTILINE)
        # 提取 slide 编号
        slides = re.findall(r"<!-- Slide number: (\d+) -->", content)

        chapter = fname.replace(".md", "")
        print(f"\n{'='*50}")
        print(f"  {chapter}  ({len(slides)} 张幻灯片)")
        print(f"{'='*50}")
        if titles:
            for t in titles[:20]:
                print(f"    {t[:80]}")
            if len(titles) > 20:
                print(f"    ... 还有 {len(titles) - 20} 个标题")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    if sys.argv[1] == "--toc":
        show_toc()
        return

    keyword = sys.argv[1]
    context = 1
    chapter = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "-C" and i + 1 < len(sys.argv):
            context = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--chapter" and i + 1 < len(sys.argv):
            chapter = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    if chapter:
        search_chapter(keyword, chapter, context)
    else:
        search_all(keyword, context)


if __name__ == "__main__":
    main()
