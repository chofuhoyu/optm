# Spec: notes-print.pdf — 考场用 A4 课堂笔记

**日期**: 2026-06-21
**状态**: 已批准，待实现

---

## 1. 动机

考试规则变化：开卷考试允许携带"课堂笔记"。现有的 `review-reader.pdf` 含有大量自编例题和 2025 真题解答，属于"习题解答/试题解答"范畴，不能带入考场。

需要一个**纯方法参考**的 A4 打印版——只包含定义、定理（无证明）、算法步骤、公式，不含任何例题或真题。

## 2. 产品

**`latex/notes-print.pdf`** — A4 双栏打印版，15-25 页，纯方法速查。

由 `make notes-print` 编译。

## 3. 文件结构

```
latex/notes/
├── notes-print.tex          ← 主入口（文档类、宏包、双栏布局）
├── notes-ch01.tex           ← 第1章 LP标准型与基本性质
├── notes-ch02.tex           ← 第2章 单纯形法
├── notes-ch03.tex           ← 第3章 对偶理论
├── notes-ch04.tex           ← 第4章 灵敏度分析
├── notes-ch05.tex           ← 第5章 凸集与凸函数
├── notes-ch06.tex           ← 第6章 最优性条件（FJ/KKT）
├── notes-ch07.tex           ← 第7章 非线性对偶
├── notes-ch08.tex           ← 第8章 无约束优化方法
└── notes-ch09.tex           ← 第9章 约束优化方法（可行方向+罚函数）
```

主入口 `notes-print.tex` 用 `\input{notes/notes-ch01.tex}` 引入各章。

## 4. 内容边界（硬规则）

### ✅ 保留

- 定义（`\textbf{定义 N.M（…）}`）
- 定理陈述，仅结论不证明（`\textbf{定理 N.M}` + 公式）
- 算法步骤（`enumerate` 枚举）
- 核心公式（`\[ ... \]` 或 `align*`）
- 方法对比表（`tabular`，如 FJ vs KKT）
- 速查条目（`itemize` 列表）
- PPT 页码引用（行内小字，如 `（课件 p7.17）`）

### ❌ 删除（从 review 中剔除）

- 所有证明（包括"证明直觉"、"证明思路"）
- 所有数字例题（自编例 + 真题）
- 所有 TikZ 几何图
- 因果解释段落（"为什么这样做"、"从何而来"）
- `defbox` / `notebox` / `examquestion` 环境
- `\refslide` 命令（替换为行内文字引用）

### 判断原则

**内容只回答"是什么"（定义、定理、公式、步骤），不回答"为什么"（证明、推导）和"怎么用"（例题、真题）。**

## 5. 排版规格

| 参数 | 值 |
|------|-----|
| 文档类 | `ctexart` |
| 字号 | 10pt |
| 纸张 | A4 |
| 页边距 | 14mm 四周 |
| 分栏 | `twocolumn`，栏间距 8mm |
| 行距 | 默认（不压缩） |
| 标题 | `\section{第N章 …}` + `\subsection{知识点}` |
| 装饰 | 无 fancy 框，纯文本 + `\textbf` 加粗 |

不显示页码（`\pagestyle{empty}`）。

## 6. 与 review 的关系

```
review-chXX.tex  ──提取纯方法内容──▶  notes-chXX.tex
```

- **notes 是 review 的严格子集**：只从 review 中删内容，不新增、不改写
- 初始创建：逐章阅读 `review-chXX.tex`，复制符合规则的内容到 `notes-chXX.tex`
- 后续维护：修改 review 某章后，必须检查对应 notes 章是否需要同步更新

## 7. 构建

```makefile
# Makefile 新增
notes: latex/notes-print.pdf

latex/notes-print.pdf: latex/notes/notes-print.tex $(wildcard latex/notes/notes-ch*.tex)
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex
```

- `make notes-print` 编译 notes-print.pdf
- `make all` 包含 notes-print（all = slides-print + slides-reader + review-reader + notes-print）
- `make clean` 加入 `latex/notes/*.aux` 等辅助文件清理

## 8. CLAUDE.md 补充

在 CLAUDE.md 中新增一段 `### 考场笔记（notes-print）`：

- 说明用途：开卷考试课堂笔记，A4 打印版
- 列出内容边界（保留/删除清单）
- 强调与 review 的同步规则：改 review 必须检查 notes
- 编译命令：`make notes-print`

## 9. 验收标准

1. `make notes-print` 编译零错误
2. `latex/notes-print.log` 无 Overfull hbox 警告（双栏窄宽度下特别注意长公式）
3. 输出 15-25 页
4. 逐章核对：不含任何例题、真题、证明
5. 所有公式、算法步骤与 review 一致（无转录错误）
6. CLAUDE.md 已更新

## 10. 实现顺序

1. 创建 `notes-print.tex` 主入口（双栏布局 + 宏包）
2. 逐章创建 `notes-ch01.tex` ~ `notes-ch09.tex`（从 review 提取）
3. 更新 Makefile（`make notes-print` + `make clean`）
4. 编译 → 检查 Overfull → 修复
5. 更新 CLAUDE.md
6. `git add -A && git commit`
