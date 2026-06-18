# 一键编译 paper.pdf
# 用法: make

.PHONY: all clean generate

all: paper.pdf

paper.pdf: main.tex chapters.tex
	xelatex -interaction=nonstopmode main.tex
	xelatex -interaction=nonstopmode main.tex

generate:
	uv run python scripts/generate_chapters.py

clean:
	rm -f main.aux main.log main.out paper.pdf
