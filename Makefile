# 编译与推送
# 用法:
#   make all          — 编译全部
#   make print        — 仅打印版
#   make reader       — 仅阅读器版
#   make generate     — 重新生成 latex/chapters.tex
#   make push-boox    — 推送阅读器版到 BOOX
#   make clean        — 清理辅助文件

.PHONY: all print reader generate push-boox clean

all: print reader review

# === 打印版（8张/页 A4）===
print: latex/slides-print.pdf

latex/slides-print.pdf: latex/slides-print.tex latex/chapters.tex
	cd latex && xelatex -interaction=nonstopmode slides-print.tex
	cd latex && xelatex -interaction=nonstopmode slides-print.tex

# === 课件阅读器版（2张/页 Leaf5）===
reader: latex/slides-reader.pdf

latex/slides-reader.pdf: latex/slides-reader.tex latex/chapters.tex
	cd latex && xelatex -interaction=nonstopmode slides-reader.tex
	cd latex && xelatex -interaction=nonstopmode slides-reader.tex

# === 复习材料阅读器版 ===
review: latex/review-reader.pdf

latex/review-reader.pdf: latex/review-reader.tex latex/review-content.tex
	cd latex && xelatex -interaction=nonstopmode review-reader.tex
	cd latex && xelatex -interaction=nonstopmode review-reader.tex

# === 生成共享章节数据 ===
generate:
	uv run python scripts/generate_filtered.py

# === 推送到 BOOX ===
push-boox: latex/slides-reader.pdf latex/review-reader.pdf
	curl -s -X POST "http://10.29.214.150:8085/api/storage/upload" \
		-F "file=@latex/slides-reader.pdf"
	curl -s -X POST "http://10.29.214.150:8085/api/storage/upload" \
		-F "file=@latex/review-reader.pdf"

# === 清理 ===
clean:
	rm -f latex/*.aux latex/*.log latex/*.out latex/*.toc
