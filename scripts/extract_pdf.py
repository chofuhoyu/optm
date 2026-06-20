"""
PDF 数学公式提取脚本 —— 基于 Pix2Text
将 PDF 转换为 Markdown + LaTeX 数学公式

用法:
    uv run python scripts/extract_pdf.py material/最优化25参考答案.pdf
    uv run python scripts/extract_pdf.py material/最优化25参考答案.pdf -o exam_2025.md
    uv run python scripts/extract_pdf.py material/最优化25参考答案.pdf --pages 0,1,2
    uv run python scripts/extract_pdf.py material/最优化25参考答案.pdf --no-combine

依赖:
    pix2text (>=1.2)  — 首次运行自动下载模型（~300-500MB）到 ~/.pix2text/
"""

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="用 Pix2Text 将 PDF 转为 Markdown（数学公式以 LaTeX 嵌入）"
    )
    parser.add_argument(
        "input",
        help="输入 PDF 文件路径",
    )
    parser.add_argument(
        "-o", "--output",
        help="输出 Markdown 文件路径（默认与输入同名的 .md 文件）",
    )
    parser.add_argument(
        "--pages",
        help="指定页码，逗号分隔（0-indexed），如 0,1,2。默认处理全部页面",
    )
    parser.add_argument(
        "--output-dir",
        help="Pix2Text 中间分页输出目录（默认自动生成，如 xxx_p2t_output/）",
    )
    parser.add_argument(
        "--no-combine",
        action="store_true",
        help="不合并为单文件，保留 Pix2Text 的分页 .md 输出",
    )
    parser.add_argument(
        "--resized-shape",
        type=int,
        default=768,
        help="处理前将页面宽度调整为该像素值（默认 768）",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：文件不存在 — {input_path}")
        sys.exit(1)
    if not input_path.suffix.lower() == ".pdf":
        print(f"错误：仅支持 PDF 文件，收到 — {input_path.suffix}")
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".md")

    # Pix2Text 分页输出目录
    if args.output_dir:
        md_dir = Path(args.output_dir)
    else:
        md_dir = input_path.parent / f"{input_path.stem}_p2t_output"

    # 解析页码
    page_numbers = None
    if args.pages:
        page_numbers = [int(p.strip()) for p in args.pages.split(",")]

    # 调用 Pix2Text
    from pix2text import Pix2Text

    print("正在初始化 Pix2Text（首次运行需下载模型 ~300-500MB，请稍候）...")
    p2t = Pix2Text.from_config()

    print(f"正在处理: {input_path}")
    if page_numbers:
        print(f"  页码范围 (0-indexed): {page_numbers}")
    else:
        print("  处理全部页面")

    doc = p2t.recognize_pdf(
        str(input_path),
        page_numbers=page_numbers,
        table_as_image=True,
    )

    # 输出 Markdown
    if args.no_combine:
        doc.to_markdown(str(md_dir))
        print(f"分页输出已保存到: {md_dir}/")
    else:
        doc.to_markdown(str(md_dir))
        md_files = sorted(md_dir.glob("*.md"))
        if not md_files:
            print("错误：Pix2Text 未生成任何 Markdown 文件")
            sys.exit(1)

        # 合并所有页面到单个文件
        with open(output_path, "w", encoding="utf-8") as out:
            for i, md_file in enumerate(md_files):
                content = md_file.read_text(encoding="utf-8")
                # 修复图片路径：反斜杠→正斜杠
                content = content.replace("figures\\", "figures/")
                if i > 0:
                    out.write("\n\n")
                out.write(content)

        # 复制 figures 目录到输出文件旁边（供 Markdown 图片引用）
        src_figures = md_dir / "figures"
        dst_figures = output_path.parent / "figures"
        if src_figures.exists():
            import shutil
            if dst_figures.exists():
                shutil.rmtree(dst_figures)
            shutil.copytree(src_figures, dst_figures)
            print(f"图片已复制到: {dst_figures}/")

        print(f"合并输出: {output_path}")
        print(f"分页中间文件保留在: {md_dir}/")


if __name__ == "__main__":
    main()
