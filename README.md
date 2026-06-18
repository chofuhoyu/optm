# 最优化理论与算法 — 开卷考试参考资料

## 项目结构

```
├── material/                  # 老师课件（原始 PDF，不动）
│   ├── 1引言.pdf
│   ├── 2数学基础.pdf
│   ├── ...（共14章）
│   └── 13罚函数法(4).pdf      # 第13章版本2
│
├── main.tex                   # LaTeX 主文件（排版模板）
├── chapters.tex               # 自动生成的章节内容（可手动编辑插入笔记）
│
├── notes/                     # 你的笔记（.tex 片段）
│   └── (示例: 1引言-notes.tex)
│
├── scripts/
│   └── generate_chapters.py   # 重新生成 chapters.tex（如课件有变动）
│
├── paper.pdf                  # 最终打印的 PDF
└── Makefile                   # 一键编译
```

## 快速开始

### 1. 编译 PDF
```bash
make          # 编译两次（解决交叉引用）
# 或手动：
xelatex main.tex && xelatex main.tex
```

### 2. 添加自己的笔记

打开 `chapters.tex`，在每章的笔记插入点添加内容：

- **单个笔记格**（混在幻灯片网格里）:
  ```latex
  \ncell{
    \textbf{单纯形法步骤} \\
    \begin{enumerate}
      \item 初始化基本可行解
      \item 计算检验数
      \item ...
    \end{enumerate}
  }
  ```

- **整页笔记**（双线大框，适合章末总结）:
  ```latex
  \notefullpage{
    \section*{第5章 单纯形方法 要点}
    ...
  }
  ```

### 3. 如果课件 PDF 有变动
```bash
uv run python scripts/generate_chapters.py   # 重新生成 chapters.tex
```

## 排版规格

- 纸张: A4, 5mm 页边距
- 布局: 2列 × 4行 = 8张幻灯片/页
- 老师幻灯片: ═══ 单线框 ═══
- 你的笔记:   ═══ 双线框 ═══
