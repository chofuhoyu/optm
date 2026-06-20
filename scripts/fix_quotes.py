"""
修复 review 章节 .tex 文件中的双引号：将 ASCII 直引号 " 替换为中文左右配对引号 " 和 "
策略：逐文件扫描，用状态机追踪引号开关，交替替换为左右引号。
"""
import os
import sys

REVIEW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "latex", "review")

# 需要跳过引号替换的行/环境
SKIP_PATTERNS = [
    # LaTeX 命令中的引号（如 \setmainfont{"FandolKai"} 之类）
    # 我们的文件里没有这种用法，但保留检查
]

def fix_quotes_in_file(filepath):
    """修复单个文件中的双引号：先处理 \" 转义，再配对替换"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 预处理：\" 是 LaTeX 中非标准的引号转义，把 \" 还原为普通 " 以便统一处理
    content = content.replace('\\"', '"')

    # 按行处理，跨行保持引号状态
    lines = content.split('\n')
    new_lines = []
    in_quote = False

    for line in lines:
        new_chars = []
        i = 0
        while i < len(line):
            c = line[i]

            if c == '"':
                if in_math_mode(line, i):
                    new_chars.append(c)
                else:
                    if not in_quote:
                        new_chars.append('“')  # " (U+201C)
                        in_quote = True
                    else:
                        new_chars.append('”')  # " (U+201D)
                        in_quote = False
            else:
                new_chars.append(c)

            i += 1

        new_lines.append(''.join(new_chars))

    new_content = '\n'.join(new_lines)

    if new_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def in_math_mode(line, pos):
    """检查位置 pos 是否在 LaTeX 数学模式中（$...$ 或 $$...$$）

    $$...$$ 算一个 toggle 单位，$...$ 中每个 $ 算一个 toggle。
    奇数个 toggle 说明当前在数学模式内。
    """
    before = line[:pos]
    toggles = 0  # 数学模式切换次数
    i = 0
    while i < len(before):
        # 跳过转义字符 \$
        if before[i] == '\\' and i + 1 < len(before) and before[i+1] == '$':
            i += 2
            continue
        if before[i] == '$':
            if i + 1 < len(before) and before[i+1] == '$':
                # display math: $$ 作为一个 toggle
                toggles += 1
                i += 2
                continue
            else:
                # inline math: 单个 $
                toggles += 1
        i += 1

    return toggles % 2 == 1


def count_quotes_in_file(filepath):
    """统计文件中的 ASCII 引号数量"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content.count('"')


def main():
    tex_files = sorted([
        f for f in os.listdir(REVIEW_DIR)
        if f.endswith('.tex')
    ])

    total_before = 0
    total_after = 0
    fixed_files = []

    for filename in tex_files:
        filepath = os.path.join(REVIEW_DIR, filename)
        before = count_quotes_in_file(filepath)
        total_before += before

        if before > 0:
            changed = fix_quotes_in_file(filepath)
            if changed:
                after = count_quotes_in_file(filepath)
                total_after += after
                fixed_files.append((filename, before, after))
                print(f"  [OK] {filename}: {before} -> {after} ASCII quotes replaced")
            else:
                print(f"  [SKIP] {filename}: no change needed")

    print(f"\nTotal: {total_before} -> {total_after} ASCII straight quotes replaced with paired Chinese quotes")

    if total_after > 0:
        print("\n[WARN] Unpaired quotes remaining! Check for multi-line quotes.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
