# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目目标

北邮"最优化理论与算法"研究生课程**开卷考试**备考项目。核心产出是一份可打印的 A4 紧凑排版 PDF（2列×4行=8张/页），从老师课件中按考试重点筛选页面，混入用户自己的手写笔记。

- 用户：姚祉圻，学号 2025018017
- 授课教师：帅天平
- 考试形式：开卷，100分 = 线性规划 50分 + 非线性规划 50分
- 远程：`git@github.com:chofuhoyu/optm.git`（`git remote -v` 中名为 origin）

## 核心规则

### Git
- **每完成一件事立即 `git add -A && git commit`**
- **严禁自行 `git push`，除非用户明确指示推送**
- 不允许批量提交多个不相关的改动
- 提交信息用中文

### 文件追踪
- `.pptx` 和 `.pdf` 都纳入 git 追踪
- `.gitignore` 仅排除：`.venv/`、`__pycache__/`、`*.aux`、`*.log`、`*.out` 等

### 工作语言
- 所有解释、注释用中文
- git 提交信息用中文
- 代码标识符保持英文

---

## 常用命令

```bash
# PPTX → PDF 批量转换（需要 Windows + PowerPoint）
uv run python scripts/pptx_to_pdf.py

# 生成/更新 chapters.tex（根据 filter_config.json）
uv run python scripts/generate_filtered.py

# 编译最终 PDF
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex   # 跑两遍

# 全文搜索课件内容
uv run python scripts/search_notes.py "关键词"           # 全部章节搜索
uv run python scripts/search_notes.py "KKT" --chapter 7  # 指定章节
uv run python scripts/search_notes.py --toc               # 章节目录

# 用 Playwright 控制浏览器下载课件（如需要）
uv run python scripts/download_pptx.py
```

---

## 项目架构

### 数据流

```
material/*.pptx          ← 老师课件（原始源文件）
    │
    ├─[win32com]──→ material/*.pdf    ← 1:1 页数对应的 PDF（LaTeX 引用）
    │
    └─[markitdown]─→ extracted/*.md   ← 每页幻灯片文字提取（可搜索）

material/考试重点.md                   ← 用户提供的考试范围
material/最优化25参考答案.pdf           ← 去年真题（有答案）

scripts/filter_config.json             ← IOE 筛选配置（JSON）
scripts/generate_filtered.py           ← 根据配置生成 chapters.tex

chapters.tex                           ← 自动生成 + 手动插笔记
main.tex                               ← LaTeX 主模板（宏定义在此）
main.pdf                               ← 最终打印输出
ioe.md                                 ← Include/Exclude 决策文档
study-plan.md                          ← 两天半复习计划
```

### LaTeX 排版规格

- 纸张 A4，5mm 页边距，不显示页码
- 2列×4行 = 8张/页，单元格带框线
- 老师幻灯片 → `\scell{文件名}{页码}` — 单线框 `\fbox`
- 用户笔记 → `\ncell{内容}` — 双线框 `\doublebox`（个别格子）
- 整页笔记 → `\notefullpage{内容}` — 双线大框占满整页
- `\slidegrid{文件}{p1}{p2}...{p8}` — 一个完整 2×4 页，页码填 0 表示空白格
- 编译用 `xelatex`（ctexart 文档类，支持中文）

### IOE 筛选系统

- `ioe.md` — 每一章的筛选决策 + 理由，格式为 SVG 表格
- `scripts/filter_config.json` — 机器可读的筛选配置，键=章节文件名前缀，值=保留的页码数组
- `scripts/generate_filtered.py` — 读取 JSON 配置，生成 8 页一组编排的 `chapters.tex`
- 修改筛选：改 `filter_config.json` → 运行 `generate_filtered.py` → 重新编译 `main.tex`

### 抽取文件说明

- `extracted/` — 每章一个 `.md`，用 `markitdown` 从 PPTX 提取
- 每页以 `<!-- Slide number: N -->` 标记
- 数学符号在文字提取中会有乱码（``=λ, ``=Δ, ``=≥, ``=∇），这是 PPT 字体编码问题，不影响语义搜索
- `scripts/search_notes.py` 支持 `-C N` 上下文行数、`--chapter N` 指定章、`--toc` 目录

---

## PPTX ↔ PDF 一致性

- 所有 PDF 由 PPTX 通过 PowerPoint COM 转换，**页数必须 1:1 对应**
- `scripts/pptx_to_pdf.py` 转换后自动核对页数
- 旧的 PDF（从课程网站直接下载的）已全部删除并用 PPTX 转换版替换
- 第13章（罚函数法）只有一份 PPTX，对应的只有一份 PDF（旧的 `13罚函数法(4).pdf` 已删除）

## 考试重点（来自 `material/考试重点.md`）

**线性规划 50分**：标准型、单纯形法（两阶段/大M）、对偶单纯形法、灵敏度分析、互补松弛、LP基本性质
**非线性规划 50分**：凸集凸函数、KKT条件、强对偶定理、共轭梯度法、拟牛顿法、可行方向法、罚函数法

基于此，筛选结果：848页 → 439页（52%），整章排除第11章（无约束直接法），编译后61张A4 + 3张笔记 = 64页。

## 用户笔记

已写入 `chapters.tex` 的三张笔记：
1. **第7章末尾** — FJ条件 vs KKT条件 对比（双线整页）
2. **第10章末尾** — DFP/BFGS 拟牛顿法公式速查（双线整页）
3. **第12章末尾** — Rosen梯度投影法算法步骤 + Zoutendijk法（双线整页）
