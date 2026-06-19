"""根据 filter_config.json + notes_config.json 生成共享 latex/chapters.tex

不再为 print/reader 分别生成——两个布局通过各自定义的 \slidesdata / \notedata 解读同一份数据。
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

CHAPTERS = [
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


def generate():
    with open(os.path.join(SCRIPT_DIR, "filter_config.json"), "r", encoding="utf-8") as f:
        slides = json.load(f)

    with open(os.path.join(SCRIPT_DIR, "notes_config.json"), "r", encoding="utf-8") as f:
        notes = json.load(f)

    output_path = os.path.join(PROJECT_DIR, "latex", "slides", "chapters.tex")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    total = 0
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("% 共享章节数据 — 由 scripts/filter_config.json + notes_config.json 生成\n")
        f.write("% 各布局（print/reader）自行定义 \\slidesdata 和 \\notedata 来解读\n\n")

        for ch_key, ch_name in CHAPTERS:
            pages = slides.get(ch_key, [])
            total += len(pages)

            f.write(f"\n% ==== {ch_name}（{len(pages)} 页）====\n")
            page_list = ",".join(str(p) for p in pages)
            f.write(f"\\slidesdata{{{ch_key}}}{{{page_list}}}\n")

            if ch_key in notes:
                note_text = notes[ch_key]
                f.write(f"\\notedata{{{ch_key}}}{{{note_text}}}\n")

        print(f"已生成: {output_path}")
        print(f"总计: {total} 页幻灯片")


if __name__ == "__main__":
    generate()
