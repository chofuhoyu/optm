# 编译所有 PDF
# 用法:
#   make all          — 编译全部
#   make print        — 仅打印版（slides-print.pdf）
#   make reader       — 仅阅读器版（slides-reader.pdf）
#   make generate     — 重新生成 chapters-*.tex
#   make push-boox    — 推送阅读器版到 BOOX
#   make clean        — 清理辅助文件

.PHONY: all print reader generate push-boox clean

all: print reader

# === 打印版（8张/页 A4）===
print: slides-print.pdf

slides-print.pdf: slides-print.tex chapters-print.tex
	xelatex -interaction=nonstopmode slides-print.tex
	xelatex -interaction=nonstopmode slides-print.tex

# === 阅读器版（2张/页 Leaf5）===
reader: slides-reader.pdf

slides-reader.pdf: slides-reader.tex chapters-reader.tex
	xelatex -interaction=nonstopmode slides-reader.tex
	xelatex -interaction=nonstopmode slides-reader.tex

# === 重新生成章节 ===
generate:
	uv run python scripts/generate_filtered.py
	uv run python scripts/generate_reader.py

# === 推送到 BOOX ===
push-boox: slides-reader.pdf
	curl -s -X POST "http://10.29.214.150:8085/api/storage/upload" \
		-F "file=@slides-reader.pdf"

# === 清理 ===
clean:
	rm -f *.aux *.log *.out *.toc
