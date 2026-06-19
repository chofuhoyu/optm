"""核实 review 各章 \refslide 引用对应的 PPT 内容。
提取所有 \refslide{章节名}{页码}{标签}，查找 extracted/ 中对应页的文字摘要。
用法: uv run python scripts/verify_slides.py [--chapter 1]
"""
import re
import sys
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REVIEW_DIR = PROJECT_DIR / "latex" / "review"
EXTRACTED_DIR = PROJECT_DIR / "extracted"


def find_slides_in_file(filepath: Path) -> list[tuple[str, int, str, int]]:
    """返回 [(章节名, 页码, 标签, 行号), ...]"""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    results = []
    for i, line in enumerate(lines, 1):
        matches = re.findall(r'\\refslide\{([^}]+)\}\{(\d+)\}\{([^}]+)\}', line)
        for ch, page, label in matches:
            results.append((ch, int(page), label, i))
    return results


def extract_slide_content(chapter_name: str, page: int) -> str | None:
    """从 extracted/ 读取对应页的文字内容"""
    md_path = EXTRACTED_DIR / f"{chapter_name}.md"
    if not md_path.exists():
        return None

    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    # 查找 <!-- Slide number: N --> 标记
    pattern = rf'<!-- Slide number: {page} -->\n(.*?)(?=<!-- Slide number:|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # 截取前 200 字符作为摘要
        return text[:300]
    return None


def main():
    target_chapter = None
    if '--chapter' in sys.argv:
        idx = sys.argv.index('--chapter')
        if idx + 1 < len(sys.argv):
            target_chapter = sys.argv[idx + 1]

    chapter_files = sorted(REVIEW_DIR.glob("review-ch*.tex"))
    if target_chapter:
        chapter_files = [f for f in chapter_files if f"ch{target_chapter.zfill(2)}" in f.name]

    total_refs = 0
    matched = 0
    mismatched = 0

    for ch_file in chapter_files:
        refs = find_slides_in_file(ch_file)
        if not refs:
            continue

        print(f"\n{'='*60}")
        print(f"📄 {ch_file.name} — {len(refs)} 处引用")
        print(f"{'='*60}")

        for ch_name, page, label, line_num in refs:
            total_refs += 1
            content = extract_slide_content(ch_name, page)

            print(f"\n  行{line_num}: \\refslide{{{ch_name}}}{{{page}}}{{{label}}}")

            if content:
                matched += 1
                # 截取前 150 字符
                preview = content[:200].replace('\n', ' ')
                print(f"  ✅ PPT内容: {preview}...")
            else:
                mismatched += 1
                if not (EXTRACTED_DIR / f"{ch_name}.md").exists():
                    print(f"  ❌ extracted/{ch_name}.md 不存在")
                else:
                    print(f"  ⚠️  页码 {page} 在 extracted/{ch_name}.md 中未找到")

    print(f"\n{'='*60}")
    print(f"总计: {total_refs} 处引用, {matched} 匹配, {mismatched} 未匹配")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
