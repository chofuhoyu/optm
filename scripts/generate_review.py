"""从 review-source.tex + filter_config.json 生成 latex/review-content.tex

解析逻辑：找到每个 \reviewstep，逐字符计数花括号深度提取参数。
"""

import json, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE = os.path.join(PROJECT_DIR, "latex", "review-source.tex")
OUTPUT = os.path.join(PROJECT_DIR, "latex", "review-content.tex")

BS = chr(92)


def load_mappings():
    with open(os.path.join(SCRIPT_DIR, "filter_config.json"), "r", encoding="utf-8") as f:
        config = json.load(f)
    return {ch: {p: i for i, p in enumerate(pages, 1)} for ch, pages in config.items()}


def extract_braced(content, pos):
    """从 content[pos] 开始提取一个 {...} 组，返回 (内容, 新位置)"""
    if pos >= len(content) or content[pos] != "{":
        raise ValueError(f"Expected {{ at pos {pos}, got {repr(content[pos:pos+10])}")
    depth = 1
    start = pos
    pos += 1
    while depth > 0 and pos < len(content):
        if content[pos] == "{":
            depth += 1
        elif content[pos] == "}":
            depth -= 1
        pos += 1
    return content[start + 1 : pos - 1], pos


def compute_label(ch, page_str, mappings):
    """根据章节名和原始页码计算标签，如 4线性规划基本性质 + 3 -> 4.1"""
    page_int = int(page_str)
    page_map = mappings.get(ch, {})
    ch_num = re.match(r"(\d+)", ch).group(1)
    return f"{ch_num}.{page_map[page_int]}" if page_int in page_map else f"{ch_num}.{page_int}"


def generate():
    mappings = load_mappings()

    with open(SOURCE, "r", encoding="utf-8") as f:
        content = f.read()

    TAG = BS + "reviewstep{"
    out_parts = []
    i = 0
    step_count = 0
    slide_count = 0

    while i < len(content):
        # 查找下一个 \reviewstep{
        if content[i : i + len(TAG)] == TAG and (i == 0 or content[i - 1] != "%"):
            i += len(TAG) - 1  # 停在 { 上

            # 提取标题 {title}
            title, i = extract_braced(content, i)

            # 跳过空白
            while i < len(content) and content[i] in " \t\n\r":
                i += 1

            # 提取答案 {answer}
            answer, i = extract_braced(content, i)

            while i < len(content) and content[i] in " \t\n\r":
                i += 1

            # 提取解读 {commentary}
            commentary, i = extract_braced(content, i)

            # 提取可变数量的 {ch}{page} 对
            slides = []
            while i < len(content):
                while i < len(content) and content[i] in " \t\n\r":
                    i += 1
                if i >= len(content) or content[i] != "{":
                    break
                # 可能是一个 {ch}，也可能是下一个 block
                # 尝试提取两个连续的 {...}
                try:
                    ch, after_ch = extract_braced(content, i)
                    j = after_ch
                    while j < len(content) and content[j] in " \t\n\r":
                        j += 1
                    if j < len(content) and content[j] == "{":
                        page, after_page = extract_braced(content, j)
                        # 检查 page 是否为纯数字（确认是页码而非下一个标题）
                        if page.strip().isdigit():
                            label = compute_label(ch, page, mappings)
                            slides.append((ch, page, label))
                            i = after_page
                            continue
                except ValueError:
                    pass
                break  # 不再有 {ch}{page} 对

            # 构建输出
            slide_parts = []
            for ch, page, label in slides:
                slide_parts.append(f"\\refslide{{{ch}}}{{{page}}}{{{label}}}")
            slide_list = "\\par\\vspace{4pt}".join(slide_parts) if slide_parts else ""
            slide_count += len(slides)

            out_parts.append(
                f"\\reviewstep{{{title}}}\n"
                f"  {{{answer}}}\n"
                f"  {{{commentary}}}\n"
                f"  {{{slide_list}}}"
            )
            step_count += 1
        else:
            out_parts.append(content[i])
            i += 1

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("".join(out_parts))

    print(f"已生成: {OUTPUT}")
    print(f"共 {step_count} 个步骤, {slide_count} 张PPT引用")


if __name__ == "__main__":
    generate()
