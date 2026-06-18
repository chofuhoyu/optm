"""生成 chapters.tex，按 2×4 网格排列所有幻灯片。

每章末尾预留笔记插入点。运行方式:
    uv run python scripts/generate_chapters.py
"""

import fitz
import os

MATERIAL = "material"
OUTPUT = "chapters.tex"

# 章节列表: (文件名(不含.pdf), 显示名称)
chapters = [
    ("1引言", "引言"),
    ("2数学基础", "数学基础"),
    ("3凸分析", "凸分析"),
    ("4线性规划基本性质", "线性规划基本性质"),
    ("5单纯形方法", "单纯形方法"),
    ("6对偶理论", "对偶理论"),
    ("7最优性条件", "最优性条件"),
    ("8算法", "算法"),
    ("9一维搜索", "一维搜索"),
    ("10使用导数的优化算法", "使用导数的优化算法"),
    ("11无约束优化直接方法", "无约束优化直接方法"),
    ("12可行方向法", "可行方向法"),
    ("13罚函数法", "罚函数法"),
    ("13罚函数法(4)", "罚函数法（版本2）"),
]


def generate_grid_cells(total: int, start: int) -> list[str]:
    """生成8个格子的页码字符串，超出范围的填 '0'"""
    cells = []
    for i in range(8):
        p = start + i
        cells.append(str(p) if p <= total else "0")
    return cells


def write_chapter(f, filename: str, name: str) -> int:
    """写入一个章节的所有 slidegrid，返回总页数"""
    filepath = os.path.join(MATERIAL, filename + ".pdf")
    if not os.path.exists(filepath):
        print(f"  ⚠ 文件不存在: {filepath}")
        return 0

    doc = fitz.open(filepath)
    total = doc.page_count
    doc.close()

    f.write(f"\n% ====== {name}（共 {total} 页，{ (total + 7) // 8 } 张A4） ======\n")
    f.write(f"% \\input{{notes/{filename}-notes.tex}}  % <-- 在这里插入笔记\n\n")

    page = 1
    while page <= total:
        cells = generate_grid_cells(total, page)
        args = "}{".join(cells)
        f.write(f"\\slidegrid{{{filename}}}{{{args}}}\n")
        page += 8

    # 章末笔记插入点
    f.write(f"\n% ── {name} 章末笔记插入点 ──\n")
    f.write(f"% 在这里插入 \\ncell{{...}} 或 \\notefullpage{{...}} 来添加你的笔记\n")
    f.write(f"% 示例: \\notefullpage{{\\section*{{{name} 要点总结}} ... }}\n\n")
    return total


def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("正在生成 chapters.tex ...")
    total_pages = 0

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("% ============================================================\n")
        f.write("%  chapters.tex — 自动生成，可手动编辑插入笔记\n")
        f.write("%  生成命令: uv run python scripts/generate_chapters.py\n")
        f.write("% ============================================================\n\n")

        for filename, name in chapters:
            pages = write_chapter(f, filename, name)
            total_pages += pages
            if pages > 0:
                print(f"  {name}: {pages} 页 → {(pages + 7) // 8} 张 A4")

    print(f"\n共 {total_pages} 张幻灯片，约 {(total_pages + 7) // 8} 张 A4 纸（不含笔记）")
    print(f"已写入: {OUTPUT}")


if __name__ == "__main__":
    main()
