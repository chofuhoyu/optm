"""快速查询 filter_config.json 中某章某页的标签序号。
用法: uv run python scripts/compute_label.py "4线性规划基本性质" 3
输出: 4.1
"""
import json
import sys
import re

def compute_label(chapter_name: str, page: int, config_path: str = "scripts/filter_config.json") -> str:
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)

    pages = config.get(chapter_name)
    if pages is None:
        raise KeyError(f"章节 '{chapter_name}' 不在 filter_config.json 中")

    try:
        idx = pages.index(page)
    except ValueError:
        available = pages[:5]
        raise ValueError(f"页码 {page} 不在章节 '{chapter_name}' 的列表中。前5个: {available}")

    # 从章节名提取章节号
    m = re.match(r'^(\d+)', chapter_name)
    if not m:
        raise ValueError(f"无法从章节名 '{chapter_name}' 提取章号")

    ch_num = m.group(1)
    return f"{ch_num}.{idx + 1}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: uv run python scripts/compute_label.py <章节名> <页码>")
        print("示例: uv run python scripts/compute_label.py '4线性规划基本性质' 3")
        sys.exit(1)

    chapter = sys.argv[1]
    page = int(sys.argv[2])
    try:
        label = compute_label(chapter, page)
        print(label)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
