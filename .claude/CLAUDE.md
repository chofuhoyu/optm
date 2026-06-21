# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目目标

北邮"最优化理论与算法"研究生课程**开卷考试**备考项目。核心产出：
- **slides-print.pdf** — A4 打印版（2列×4行=8张/页），考试用
- **slides-reader.pdf** — Leaf5 课件阅读器版（2张/页，适配 1680×1264 屏幕）
- **review-reader.pdf** — Leaf5 复习材料（按知识点编排，2025真题作为例题嵌入）

- 用户：姚祉圻，学号 2025018017
- 授课教师：帅天平
- 考试形式：开卷，100分 = 线性规划 50分 + 非线性规划 50分
- 远程：`git@github.com:chofuhoyu/optm.git`（`git remote -v` 中名为 origin）

## 核心规则

### Git
- **每完成一件事立即 `git add -A && git commit`**
- **严禁自行 `git push`，除非用户明确指示推送**
- **`git push` 后紧接着 `make push-review`**（若课件有改动也 `make push-slides`），确保 BOOX 阅读器同步最新 PDF
- 不允许批量提交多个不相关的改动
- 提交信息用中文

### 文件追踪
- `.pptx` 和 `.pdf` 都纳入 git 追踪
- `.gitignore` 排除：`.venv/`、`__pycache__/`、`*.aux`、`*.log`、`*.out`、`latex/*.pdf`、`material/*_p2t_output/`

### 编译
- **`make` 命令严禁后接任何管道**（`|`、`2>&1`、`>/dev/null` 等），必须直接运行并阅读完整输出
- 编译后必须检查 `latex/review-reader.log`（或对应 `.log`）中的 Overfull/Underfull 警告
- 发现 Overfull 必须修复。**严禁用 `\small`/`\footnotesize`/`\scriptsize` 缩小字号来消除溢出**——正确做法是换行（`\\`、`aligned`、`align*`、`multline` 等）或拆分长公式

### 工作语言
- 所有解释、注释用中文
- git 提交信息用中文
- 代码标识符保持英文

---

## 常用命令

```bash
# === 编译（全部使用 make） ===
make all           # 编译全部 3 个 PDF（print + reader + review）
make print         # 仅 A4 打印版 slides-print.pdf（8张/页）
make reader        # 仅课件阅读器版 slides-reader.pdf（2张/页，适配 Leaf5）
make review        # 仅复习材料 review-reader.pdf（真题答案 + 解读 + 课件）

# === 生成共享数据 ===
make generate      # 重新生成 latex/slides/chapters.tex（根据 filter_config.json + notes_config.json）

# === 提取 ===
make extract-exam  # 用 Pix2Text 提取 material/最优化25参考答案.pdf → exam_2025.md（含 LaTeX 数学公式）

# === 推送到 BOOX 阅读器 ===
make push          # 推送全部（课件 + 复习材料）
make push-slides   # 仅推送课件 slides-reader.pdf
make push-review   # 仅推送复习材料 review-reader.pdf

# === 工具脚本 ===
uv run python scripts/pptx_to_pdf.py                     # PPTX→PDF 批量转换（需 Windows + PowerPoint）
uv run python scripts/search_notes.py "关键词"            # 全文搜索课件内容
uv run python scripts/search_notes.py "KKT" --chapter 7   # 指定章节搜索
uv run python scripts/search_notes.py --toc                # 章节目录
uv run python scripts/download_pptx.py                    # Playwright 下载课件（如需要）
uv run python scripts/compute_label.py "4线性规划基本性质" 3  # 计算某章某页的标签序号（如 4.1）
uv run python scripts/verify_slides.py                    # 核实 review 各章 \refslide 引用的 PPT 内容
uv run python scripts/verify_ch06.py                      # 验证 review-ch06.tex 中所有数学例子
uv run python scripts/verify_ch08.py                      # 验证 review-ch08.tex 中所有数学例子
uv run python scripts/fix_quotes.py                       # 修复 review .tex 文件中的 ASCII 引号为中文配对引号
uv run python scripts/extract_pdf.py "PDF文件"             # Pix2Text PDF→Markdown+LaTeX 提取（数学公式识别）
uv run python scripts/extract_pdf.py "PDF" --pages 0,1,2   # 指定页码范围提取

# === 其他 ===
make clean         # 清理所有 *.aux *.log *.out *.toc（slides/ + review/ + review-old/）
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
    │
    └─[Pix2Text]──→ exam_2025.md       ← 真题 PDF 提取（Markdown + LaTeX 数学公式，可读！）

scripts/filter_config.json             ← IOE 筛选配置（保留页码）
scripts/notes_config.json              ← 用户手写笔记内容（按章节键索引）
scripts/generate_filtered.py           ← 读 JSON → 生成共享数据

latex/slides/chapters.tex              ← 自动生成：\slidesdata{ch}{pages} + \notedata{ch}{content}
latex/slides/slides-print.tex          ← A4 打印版入口（8张/页，自定义 \slidesdata/\notedata）
latex/slides/slides-reader.tex         ← Leaf5 课件阅读器版入口（2张/页，自定义 \slidesdata/\notedata）

latex/review/review-reader.tex         ← Leaf5 复习材料入口
latex/review/review-ch01.tex           ← 第1章 LP标准型与基本性质（手工编写）
latex/review/review-ch02.tex           ← 第2章 单纯形法
latex/review/review-ch03.tex           ← 第3章 对偶理论
latex/review/review-ch04.tex           ← 第4章 灵敏度分析
latex/review/review-ch05.tex           ← 第5章 凸集与凸函数（非线性部分开始）
latex/review/review-ch06.tex           ← 第6章 最优性条件（FJ与KKT）
latex/review/review-ch07.tex           ← 第7章 非线性对偶
latex/review/review-ch08.tex           ← 第8章 无约束优化方法
latex/review/review-ch09.tex           ← 第9章 约束优化方法（可行方向+罚函数）

latex/review-old/                      ← 旧版复习材料（review-source + review-content 模式，已废弃）
ioe.md                                 ← 各章 Include/Exclude 决策文档（SVG表格）
study-plan.md                          ← 两天半复习计划
exam_2025.md                           ← 2025年真题参考答案（Pix2Text 提取，含 LaTeX 公式，可读！）
exam_2025.txt                          ← 旧版（纯文本提取，乱码严重，已废弃）
```

### 共享数据机制（核心设计）

两个课件布局（print 和 reader）通过 LaTeX3 宏共享同一份数据源 `chapters.tex`：

- `chapters.tex` 使用 `\slidesdata{章节名}{页码列表}` 声明每章的幻灯片页码
- `chapters.tex` 使用 `\notedata{章节名}{内容}` 声明每章末尾的笔记内容
- `slides-print.tex` 定义 `\slidesdata` 为每8页编组输出一个 `\slidegrid`
- `slides-reader.tex` 定义 `\slidesdata` 为每2页编组输出一个 `\leafslidepair`
- 两个布局各自定义 `\notedata` 为适合自己的笔记页格式

修改筛选流程：`filter_config.json` → `make generate` → `make all`

### LaTeX 排版规格

**打印版（slides-print.tex）**：
- 纸张 A4，5mm 页边距，不显示页码
- `\scell{文件名}{页码}` — 老师幻灯片，单线框 `\fbox`
- `\ncell{内容}` — 用户笔记，单个格子的双线框 `\doublebox`
- `\notefullpage{内容}` — 整页笔记，双线大框
- `\slidegrid{文件}{p1}...{p8}` — 完整 2×4 页网格，页码填 0 = 空白格

**阅读器版（slides-reader.tex + review-reader.tex）**：
- 纸张 126.4mm × 168.0mm（Leaf5 屏幕比例），5mm 页边距
- `\refslide{文件名}{页码}{标签}` — 老师幻灯片 + 右上角黑色页码标签（如 2.3 = 第2章第3页PPT）
- `\leafslidepair{文件}{p1}{p2}{章号}` — 一页两张幻灯片

**复习材料（review-reader.tex）**：
- `extarticle` 14pt 字体，允许多行公式（`\emergencystretch=3em`，`\hfuzz=2pt`）
- `\refslide{文件名}{页码}{标签}` — 嵌入课件引用（路径 `../../material/`）
- `defbox` — 定理/定义/性质框（左侧黑竖线，可跨页 `breakable`）
- `notebox` — 注意/提示框（左侧灰竖线，可跨页）
- `examquestion{题号}` — 真题区块

编译均用 `xelatex`（ctexart/extarticle 文档类，支持中文）。

### IOE 筛选系统

- `ioe.md` — 每一章的筛选决策 + 理由（SVG 表格）
- `scripts/filter_config.json` — 机器可读的筛选配置，键=章节文件名前缀，值=保留的页码数组
- `scripts/generate_filtered.py` — 读取 JSON → 生成 `latex/slides/chapters.tex`
- `scripts/notes_config.json` — 用户笔记内容，键=章节名，值=LaTeX 内容（`\notedata` 标签内嵌）
- 修改筛选：改 `filter_config.json` → `make generate` → `make all`

### 抽取文件说明

- `extracted/` — 每章一个 `.md`，用 `markitdown` 从 PPTX 提取
- 每页以 `<!-- Slide number: N -->` 标记
- 数学符号在文字提取中会有乱码（``=λ, ``=Δ, ``=≥, ``=∇），这是 PPT 字体编码问题
- `scripts/search_notes.py` 支持 `-C N` 上下文行数、`--chapter N` 指定章、`--toc` 目录

### Pix2Text PDF 提取

- `scripts/extract_pdf.py` — 基于 [Pix2Text](https://github.com/breezedeus/Pix2Text) 的 PDF 提取脚本
- 流水线：布局分析 → 公式检测(MFD) → 公式识别(MFR) → Markdown+LaTeX 输出
- 首次运行自动从 HuggingFace 下载模型（~300-500MB），存于 `~/.pix2text/`
- 输出：数学公式以 `$...$`/`$$...$$` LaTeX 嵌入，中文文本 OCR，表格以图片保留
- `exam_2025.md` + `figures/` — 从 `material/最优化25参考答案.pdf` 的提取产物
- 原来的 `exam_2025.txt`（纯文本提取，乱码严重）已废弃
- `make extract-exam` 可重新生成

---

## PPTX ↔ PDF 一致性

- 所有 PDF 由 PPTX 通过 PowerPoint COM 转换，**页数必须 1:1 对应**
- `scripts/pptx_to_pdf.py` 转换后自动核对页数
- 旧的 PDF（从课程网站直接下载的）已全部删除并用 PPTX 转换版替换
- 第13章（罚函数法）只有一份 PPTX，对应的只有一份 PDF

## 复习材料架构

复习材料（`latex/review/`）已从旧版单一 `review-content.tex`（由 `generate_review.py` 从 `review-source.tex` 生成）重构为 **按知识点手工编写的 9 个独立章节文件**：

- `review-ch01.tex` — LP标准型化方法、基本可行解/极点性质、目标函数有界性、多面体多胞形、线性规划基本定理
- `review-ch02.tex` — 单纯形法思想、检验数推导、单纯形表与转轴运算、两阶段法/大M法、Bland规则、退化
- `review-ch03.tex` — 对偶问题构造（对称/非对称）、弱对偶与强对偶定理、互补松弛、对偶单纯形法、影子价格
- `review-ch04.tex` — 灵敏度分析：c变化（基变量/非基变量）、b变化、新增约束、新增变量
- `review-ch05.tex` — 凸集与凸函数：一阶/二阶判别、Hessian与凸性、凸规划性质、3层判别法递进
- `review-ch06.tex` — FJ条件（λ₀=0退化情形）、KKT条件、约束规格（LICQ/Slater）、FJ→KKT逻辑链
- `review-ch07.tex` — Lagrange对偶、弱/强对偶定理、鞍点与KKT、Wolfe对偶
- `review-ch08.tex` — 最速下降法、Newton法、共轭梯度法（FR公式）、DFP/BFGS拟牛顿法、Armijo法则
- `review-ch09.tex` — 可行方向法（Zoutendijk）、Rosen梯度投影法、罚函数法（外点/内点/乘子法）

各章风格：带有因果讲解（为什么这样做）、自编数字例题、PPT引导语（"翻到第X.Y页"），2025真题直接嵌入作为例题讲解。

旧版文件保存在 `latex/review-old/`，不再使用。

### 考场课堂笔记（notes-print）

`latex/notes/` 目录存放考场用的 A4 课堂笔记，由 `make notes` 编译输出 `latex/notes-print.pdf`。

**用途**：开卷考试带入考场，作为"课堂笔记"使用。仅含定义、定理、公式、算法步骤，不含任何例题或真题。

**内容边界（硬规则）**：
| ✅ 保留 | ❌ 删除 |
|---------|---------|
| 定义、定理陈述（不证） | 所有证明（含"证明直觉"） |
| 算法步骤（enumerate 枚举） | 所有数字例题（自编例 + 真题） |
| 核心公式 | TikZ 几何图 |
| 方法对比表 | 因果解释段落 |
| PPT 页码引用（行内小字） | defbox/notebox/examquestion 环境 |

**判断原则**：内容只回答"是什么"（定义、定理、公式、步骤），不回答"为什么"（证明、推导）和"怎么用"（例题、真题）。

**与 review 的关系**（条件编译架构）：
- `notes-print.tex` 直接 `\input{review/review-chXX.tex}`，不再手工维护独立的 notes 文件
- 通过宏覆盖实现内容过滤：`\reviewonly{...}`（notes 中吞掉）、`notebox`（吞掉）、`examquestion`（吞掉）、`tikzpicture`（吞掉）、`defbox`（简化为间距）、`\refslide`（改为小字页码）
- `review-reader.tex` 中定义 `\newcommand{\reviewonly}[1]{#1}`（原样输出）
- `notes-print.tex` 中定义 `\newcommand{\reviewonly}[1]{}`（吞掉内容）
- **修改 review 某章后，检查新增的例题/真题/因果解释/TikZ图是否在 `\reviewonly{...}` 内**
- 旧的 9 个 `notes-chXX.tex` 文件已废弃，不再使用
- 编译：`make notes`（不纳入 `make all`）

## 考试重点（来自 `material/考试重点.md`）

**线性规划 50分**：标准型、单纯形法（两阶段/大M）、对偶单纯形法、灵敏度分析、互补松弛、LP基本性质
**非线性规划 50分**：凸集凸函数、KKT条件、强对偶定理、共轭梯度法、拟牛顿法、可行方向法、罚函数法

筛选结果：848页 → 439页（52%），整章排除第11章（无约束直接法）。

## 用户笔记

笔记存储在 `scripts/notes_config.json`，在 `make generate` 时注入 `chapters.tex`：

1. **第7章末尾** — FJ条件 vs KKT条件 对比（`\notedata` 双线整页）
2. **第10章末尾** — DFP/BFGS 拟牛顿法公式速查（`\notedata` 双线整页）
3. **第12章末尾** — Rosen梯度投影法算法步骤 + Zoutendijk法（`\notedata` 双线整页）

如需增删笔记，编辑 `scripts/notes_config.json` → `make generate` → `make all`。
