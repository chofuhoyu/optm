# 编译与推送
# 用法:
#   make all            — 编译全部 4 个 PDF
#   make slides         — 编译课件（打印版 + 阅读器版）
#   make slides-print   — 课件 A4 打印版（8张/页）
#   make slides-reader  — 课件 Leaf5 阅读器版（2张/页）
#   make review-reader  — 复习材料 Leaf5 阅读器版
#   make notes-print    — 考场课堂笔记 A4 打印版
#   make generate       — 重新生成 latex/slides/chapters.tex
#   make extract-exam   — 用 Pix2Text 提取真题 PDF → exam_2025.md
#   make push           — 推送全部到 BOOX
#   make push-slides    — 推送课件到 BOOX
#   make push-review    — 推送复习材料到 BOOX
#   make clean          — 清理辅助文件

.PHONY: all slides slides-print slides-reader review-reader notes-print generate extract-exam push push-slides push-review clean

# === 全部 ===
all: slides-print slides-reader review-reader notes-print

# === 课件 ===
slides: slides-print slides-reader

# === 课件 A4 打印版（8张/页）===
slides-print: latex/slides-print.pdf

latex/slides-print.pdf: latex/slides/slides-print.tex latex/slides/chapters.tex
	cd latex && xelatex -interaction=nonstopmode slides/slides-print.tex
	cd latex && xelatex -interaction=nonstopmode slides/slides-print.tex

# === 课件 Leaf5 阅读器版（2张/页）===
slides-reader: latex/slides-reader.pdf

latex/slides-reader.pdf: latex/slides/slides-reader.tex latex/slides/chapters.tex
	cd latex && xelatex -interaction=nonstopmode slides/slides-reader.tex
	cd latex && xelatex -interaction=nonstopmode slides/slides-reader.tex

# === 复习材料 Leaf5 阅读器版 ===
review-reader: latex/review-reader.pdf

REVIEW_SRCS := $(wildcard latex/review/review-ch*.tex)
latex/review-reader.pdf: latex/review/review-reader.tex $(REVIEW_SRCS)
	cd latex && xelatex -interaction=nonstopmode review/review-reader.tex
	cd latex && xelatex -interaction=nonstopmode review/review-reader.tex

# === 考场课堂笔记 A4 打印版 ===
notes-print: latex/notes-print.pdf

NOTES_SRCS := $(wildcard latex/notes/notes-ch*.tex)
latex/notes-print.pdf: latex/notes/notes-print.tex $(NOTES_SRCS)
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex

# === 生成共享章节数据 ===
generate:
	uv run python scripts/generate_filtered.py

# === 提取真题 PDF（Pix2Text） ===
extract-exam:
	uv run python scripts/extract_pdf.py "material/最优化25参考答案.pdf" -o exam_2025.md

# === 推送到 BOOX ===
push: push-slides push-review

push-review: latex/review-reader.pdf
	curl -s -X POST "http://10.29.214.150:8085/api/storage/upload" \
		-F "file=@latex/review-reader.pdf"

push-slides: latex/slides-reader.pdf
	curl -s -X POST "http://10.29.214.150:8085/api/storage/upload" \
		-F "file=@latex/slides-reader.pdf"

# === 清理 ===
clean:
	rm -f latex/*.aux latex/*.log latex/*.out latex/*.toc
	rm -f latex/slides/*.aux latex/slides/*.log latex/slides/*.out latex/slides/*.toc
	rm -f latex/review/*.aux latex/review/*.log latex/review/*.out latex/review/*.toc
	rm -f latex/review-old/*.aux latex/review-old/*.log latex/review-old/*.out latex/review-old/*.toc
	rm -f latex/notes/*.aux latex/notes/*.log latex/notes/*.out latex/notes/*.toc
