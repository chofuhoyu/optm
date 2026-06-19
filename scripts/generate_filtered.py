"""根据 filter_config.json 生成精简版 chapters.tex"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def generate():
    with open(os.path.join(SCRIPT_DIR, "filter_config.json"), "r", encoding="utf-8") as f:
        config = json.load(f)

    chapter_names = [
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
    ]

    output_path = os.path.join(PROJECT_DIR, "chapters.tex")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("% 精简版 chapters.tex — 基于考试重点筛选\n")
        f.write(f"% 生成命令: uv run python scripts/generate_filtered.py\n")
        f.write(f"% 总页数: {sum(len(config.get(ch, [])) for ch, _ in chapter_names)}\n\n")

        for ch_key, ch_name in chapter_names:
            pages = config.get(ch_key, [])

            f.write(f"\n% ====== {ch_name}（共 {len(pages)} 页） ======\n")
            f.write(f"% \\input{{notes/{ch_key}-notes.tex}}  % <-- 章末笔记\n\n")

            if not pages:
                f.write(f"% （本章不考，已全部排除）\n\n")
                continue

            # 8页一组排进网格
            for i in range(0, len(pages), 8):
                group = pages[i:i+8]
                # 补齐到8个
                cells = [str(p) for p in group] + ["0"] * (8 - len(group))
                args = "}{".join(cells)
                f.write(f"\\slidegrid{{{ch_key}}}{{{args}}}\n")

            f.write(f"\n% ── {ch_name} 章末笔记 ──\n\n")

    print(f"已生成: {output_path}")
    total = sum(len(config.get(ch, [])) for ch, _ in chapter_names)
    grids = sum((len(config.get(ch, [])) + 7) // 8 for ch, _ in chapter_names)
    print(f"总计: {total} 页幻灯片 → {grids} 张 A4（不含笔记）")

if __name__ == "__main__":
    generate()
