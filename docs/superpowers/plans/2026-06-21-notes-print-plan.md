# notes-print.pdf 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建考场用 A4 课堂笔记 PDF——从 review 材料中提取纯方法内容（定义/定理/公式/算法），删除所有例题和真题。

**Architecture:** 新建 `latex/notes/` 目录，一个主入口 `notes-print.tex`（A4 双栏布局）+ 9 个章节文件 `notes-ch01.tex` ~ `notes-ch09.tex`，通过 `\input` 引入。Makefile 新增 `make notes-print` target。

**Tech Stack:** XeLaTeX + ctexart + amsmath + booktabs

---

## 文件结构

```
latex/notes/
├── notes-print.tex          ← 新建：主入口（文档类、宏包、双栏布局）
├── notes-ch01.tex           ← 新建：第1章 LP标准型与基本性质
├── notes-ch02.tex           ← 新建：第2章 单纯形法
├── notes-ch03.tex           ← 新建：第3章 对偶理论
├── notes-ch04.tex           ← 新建：第4章 灵敏度分析
├── notes-ch05.tex           ← 新建：第5章 凸集与凸函数
├── notes-ch06.tex           ← 新建：第6章 最优性条件（FJ/KKT）
├── notes-ch07.tex           ← 新建：第7章 非线性对偶
├── notes-ch08.tex           ← 新建：第8章 无约束优化方法
└── notes-ch09.tex           ← 新建：第9章 约束优化方法

Makefile                     ← 修改：新增 make notes-print + 扩展 make clean
CLAUDE.md                    ← 修改：新增 notes-print 章节说明
```

## 内容提取规则（每个章节文件都遵循）

**保留：**
- 定义（`\textbf{定义}`）
- 定理陈述，不证（`\textbf{定理}`）
- 算法步骤（`enumerate` 枚举）
- 核心公式（`\[ ... \]` 或 `align*`）
- 对比表（`tabular`）
- 速查条目（`itemize`）
- PPT 页码引用，转为行内小字 `（课件 pX.Y）`

**删除：**
- 所有证明（含"证明直觉"、"证明思路"）
- 所有数字例题（自编例 + 真题）
- 所有 TikZ 图
- 因果解释段落
- `defbox` / `notebox` / `examquestion` 环境
- `\refslide` 命令
- `\clearpage` / `\newpage`
- `\medskip` 多余间距

**判断原则：** 内容只回答"是什么"（定义、定理、公式、步骤），不回答"为什么"（证明、推导）和"怎么用"（例题、真题）。

---

### Task 1: 创建主入口 `notes-print.tex`

**Files:**
- Create: `latex/notes/notes-print.tex`

- [ ] **Step 1: 编写主入口文件**

```latex
% !TeX program = xelatex
% ============================================================
%  最优化理论与算法 — 考场课堂笔记（A4 打印版）
%  内容：纯方法参考（定义/定理/公式/算法步骤）
%  不含例题、真题、证明
% ============================================================
\documentclass[10pt,a4paper,twocolumn]{ctexart}

% === 页面设置 ===
\usepackage[margin=14mm,columnsep=8mm]{geometry}
\setlength{\parindent}{0pt}
\pagestyle{empty}

% === 宏包 ===
\usepackage{amsmath, amssymb}
\usepackage{booktabs}
\usepackage{enumitem}
\setlist{nosep, leftmargin=*}

% === 标题格式 ===
\ctexset{
  section = {
    format = \large\bfseries,
    beforeskip = 4pt,
    afterskip = 2pt,
  },
  subsection = {
    format = \bfseries,
    beforeskip = 3pt,
    afterskip = 1pt,
  },
}

% === 允许公式稍微溢出 ===
\setlength{\emergencystretch}{1.5em}

\begin{document}

% === 封面标题 ===
\begin{center}
{\Large 最优化理论与算法 —— 课堂笔记}

\vspace{2pt}
{\small 仅含定义、定理、公式、算法步骤。不含例题与真题。}
\end{center}

\vspace{6pt}

% === 各章内容 ===
\input{notes/notes-ch01.tex}
\input{notes/notes-ch02.tex}
\input{notes/notes-ch03.tex}
\input{notes/notes-ch04.tex}
\input{notes/notes-ch05.tex}
\input{notes/notes-ch06.tex}
\input{notes/notes-ch07.tex}
\input{notes/notes-ch08.tex}
\input{notes/notes-ch09.tex}

\end{document}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-print.tex
git commit -m "feat: notes-print 主入口文件（A4 双栏布局）"
```

---

### Task 2: 创建 `notes-ch01.tex` — LP标准型与基本性质

**Files:**
- Read: `latex/review/review-ch01.tex`（618 行，作为内容源）
- Create: `latex/notes/notes-ch01.tex`

- [ ] **Step 1: 从 review-ch01.tex 提取纯方法内容**

提取以下内容到 `latex/notes/notes-ch01.tex`：

```latex
% ============================================================
%  第1章：LP标准型与基本性质
% ============================================================
\section{第1章 \quad LP标准型与基本性质}

\subsection{标准型LP}

\textbf{定义 1.1（线性规划的一般形式）}
\[
\begin{aligned}
\min\ (\text{或}\max)\ & \sum_{j=1}^n c_j x_j \\
\text{s.t.}\ & \sum_{j=1}^n a_{ij} x_j \le b_i,\quad i\in I_1 \\
& \sum_{j=1}^n a_{ij} x_j \ge b_i,\quad i\in I_2 \\
& \sum_{j=1}^n a_{ij} x_j = b_i,\quad i\in I_3 \\
& x_j \ge 0,\quad j\in J
\end{aligned}
\]

\textbf{定义 1.2（标准型LP的四条要求）}
\begin{enumerate}
  \item[(1)] 目标函数为极小化（$\min$）
  \item[(2)] 所有约束为等式（$=$）
  \item[(3)] 所有右端常数非负（$b_i \ge 0$）
  \item[(4)] 所有变量非负（$x_j \ge 0$）
\end{enumerate}
矩阵形式：$\min\ c^T x,\ \text{s.t.}\ Ax = b,\ x \ge 0,\ b \ge 0$。

（课件 p4.1, p4.3）

\subsection{化标准型四步法}

\textbf{方法 1.1（化标准型）}
\begin{enumerate}
  \item $\max \to \min$：目标函数乘 $-1$，最优解不变，最优值变号
  \item $\le$ 约束：左端加松弛变量 $s \ge 0$。$a^T x \le b \to a^T x + s = b$
  \item $\ge$ 约束：左端减剩余变量 $s \ge 0$。$a^T x \ge b \to a^T x - s = b$
  \item 自由变量：拆成两个非负变量的差 $x_j = x_j^+ - x_j^-$，$x_j^+, x_j^- \ge 0$
  \item $b_i < 0$：约束两端乘 $-1$（不等式需翻转不等号）
\end{enumerate}

\subsection{基、基本解、基本可行解}

\textbf{定义 1.3（基、基变量、非基变量）}
设 $A$ 为 $m\times n$ 矩阵（$m<n$）。选出 $m$ 个线性无关的列组成 $m\times m$ 可逆方阵 $B$，称为一个基。对应变量为基变量 $x_B$，其余为非基变量 $x_N$。

\textbf{定义 1.4（基本解与基本可行解）}
令 $x_N = 0$，解 $Bx_B = b$ 得 $x_B = B^{-1}b$。$x = \begin{pmatrix}x_B \\ 0\end{pmatrix}$ 称为基本解。若 $x_B \ge 0$，则为基本可行解（BFS）。若某基变量恰好为 $0$，称此 BFS 为退化的。

\textbf{基本解个数上限：} $\le \binom{n}{m}$，有限个。（课件 p4.16）

\subsection{BFS与极点的等价性}

\textbf{定理 1.1（BFS $\Leftrightarrow$ 极点）}
设可行域 $S = \{x \mid Ax = b,\ x \ge 0\}$ 非空，$\mathrm{rank}(A)=m$。点 $\bar{x} \in S$ 是 $S$ 的极点当且仅当 $\bar{x}$ 是一个基本可行解。

（课件 p4.17）

\subsection{最优BFS的存在性}

\textbf{定理 1.2（最优BFS的存在性）}
若可行域非空且目标函数在可行域上有下界（最优值有限），则存在一个基本可行解是最优解。

（课件 p4.6, p4.23）

\subsection{表示定理（选读）}

\textbf{定理 1.3（表示定理）}
设 $S = \{x \mid Ax = b,\ x \ge 0\}$。$S$ 中任意点 $x$ 可表示为：
\[
x = \sum_{i=1}^{k} \lambda_i v_i + \sum_{j=1}^{\ell} \mu_j d_j
\]
其中 $v_i$ 是全部极点（BFS），$d_j$ 是全部极方向，$\lambda_i \ge 0$，$\sum\lambda_i = 1$，$\mu_j \ge 0$。
若某 $d_j$ 满足 $c^T d_j < 0$，则最优值无下界。

（课件 p4.7, p4.24）

\subsection{本章速查}

\begin{itemize}
  \item \textbf{标准型四要素}：$\min$、$=$、$b\ge 0$、$x\ge 0$
  \item \textbf{化标准型}：$\max\to\min$（乘$-1$）、$\le$（加松弛）、$\ge$（减剩余）、自由变量 $x=x^+-x^-$、$b<0$（乘$-1$）
  \item \textbf{基 $\to$ 基本解 $\to$ BFS}：选 $m$ 列 $\to$ 基 $B$ $\to$ $x_B=B^{-1}b$ $\to$ 若 $\ge 0$ 则为 BFS
  \item \textbf{BFS $\Leftrightarrow$ 极点}（定理 1.1）：代数与几何的统一
  \item \textbf{最优值有限 $\Rightarrow$ 存在最优 BFS}（定理 1.2）
  \item \textbf{表示定理}（定理 1.3）：可行域 = 极点凸组合 + 极方向锥组合
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch01.tex
git commit -m "feat: notes-ch01 LP标准型与基本性质"
```

---

### Task 3: 创建 `notes-ch02.tex` — 单纯形法

**Files:**
- Read: `latex/review/review-ch02.tex`
- Create: `latex/notes/notes-ch02.tex`

- [ ] **Step 1: 从 review-ch02.tex 提取纯方法内容**

提取定义、算法步骤（单纯形法流程、两阶段法/大M法、Bland规则）、检验数公式、转轴运算规则、退化定义。删除所有自编例题（2.5节的单纯形表迭代）和真题。

```latex
% ============================================================
%  第2章：单纯形法
% ============================================================
\section{第2章 \quad 单纯形法}

\subsection{单纯形法基本思想}

在顶点间沿棱跳跃，每一步目标值严格下降（对 $\min$ 问题）。BFS 总数有限且目标严格单调，算法必然有限步终止。
（课件 p5.1）

\subsection{转轴运算}

\textbf{定义} 从一个 BFS 出发，选择一个非基变量进基（其检验数为负，目标可进一步下降），选择一个基变量出基（保持可行性），通过行变换更新单纯形表。

\textbf{检验数（对 $\min$ 问题）：}
\[
\sigma_j = c_j - c_B^T B^{-1} a_j
\]
若所有 $\sigma_j \ge 0$，则当前 BFS 为最优解。
若存在 $\sigma_j < 0$ 但对应列 $B^{-1}a_j \le 0$，则问题无界。

\textbf{换基规则：}
\begin{itemize}
  \item \textbf{进基变量选择：} 取最小 $\sigma_j < 0$ 对应的列（也可选任意负检验数）
  \item \textbf{出基变量选择（最小比值规则）：} $\displaystyle \min\left\{\frac{(B^{-1}b)_i}{(B^{-1}a_j)_i} \;\middle|\; (B^{-1}a_j)_i > 0\right\}$
\end{itemize}

\subsection{单纯形表}

\textbf{标准表结构（$\min$ 问题）：}
\begin{center}
\begin{tabular}{c|cccc|c}
& $x_1$ & $x_2$ & $\cdots$ & $x_n$ & RHS \\
\hline
$z$ & $\sigma_1$ & $\sigma_2$ & $\cdots$ & $\sigma_n$ & $-z^*$ \\
\hline
$x_{B_1}$ & & & & & \\
$\vdots$ & & $B^{-1}A$ & & & $B^{-1}b$ \\
$x_{B_m}$ & & & & & \\
\end{tabular}
\end{center}
$c_B$ 列在最优表中给出对偶变量（影子价格）。

\subsection{初始基本可行解的构造}

\textbf{两阶段法：}
\begin{enumerate}
  \item 阶段I：引入人工变量，构造辅助问题 $\min\ \sum$人工变量，求初始 BFS
  \item 阶段II：用阶段I得到的 BFS 作为初始解，求解原问题
\end{enumerate}

\textbf{大M法：} 在原目标中加入 $M\cdot\sum$人工变量（$M$ 为充分大正数），一次求解。

\subsection{单纯形法的有限终止性}

\textbf{Bland规则（避免循环）：}
\begin{itemize}
  \item 进基：选下标最小的负检验数对应变量
  \item 出基：在比值最小的候选者中选下标最小的
\end{itemize}

\textbf{退化：} 若某个基变量取值为 $0$，称当前 BFS 退化。退化可能导致循环（Bland规则可避免）。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{检验数}：$\sigma_j = c_j - c_B^T B^{-1} a_j$。$\min$ 问题中全部 $\ge 0$ 即最优
  \item \textbf{换基}：进基取 $\sigma_j<0$，出基取最小比值
  \item \textbf{两阶段法}：阶段I构造初始BFS，阶段II求解
  \item \textbf{大M法}：添加惩罚项一次性求解
  \item \textbf{Bland规则}：选最小下标，防止循环
  \item \textbf{退化BFS}：基变量含零值
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch02.tex
git commit -m "feat: notes-ch02 单纯形法"
```

---

### Task 4: 创建 `notes-ch03.tex` — 对偶理论

**Files:**
- Read: `latex/review/review-ch03.tex`
- Create: `latex/notes/notes-ch03.tex`

- [ ] **Step 1: 从 review-ch03.tex 提取纯方法内容**

提取对偶问题的构造规则（对称/非对称）、弱对偶定理、强对偶定理、互补松弛条件、对偶单纯形法步骤、影子价格定义。删除自编例题和真题。

```latex
% ============================================================
%  第3章：对偶理论
% ============================================================
\section{第3章 \quad 对偶理论}

\subsection{对偶问题的构造}

\textbf{对称形式（$\min$ 原问题，$\le$ 约束）：}
\begin{center}
\begin{tabular}{c|c}
\textbf{原问题 (P)} & \textbf{对偶问题 (D)} \\
\hline
$\min\ c^T x$ & $\max\ b^T y$ \\
$\text{s.t.}\ Ax \ge b$ & $\text{s.t.}\ A^T y \le c$ \\
$x \ge 0$ & $y \ge 0$ \\
\end{tabular}
\end{center}

\textbf{一般构造规则：}
\begin{itemize}
  \item 原问题 $\min$ $\to$ 对偶问题 $\max$
  \item 原问题第 $i$ 约束的右端 $b_i$ $\to$ 对偶变量 $y_i$
  \item 原问题第 $j$ 变量的系数 $c_j$ $\to$ 对偶约束的右端
  \item 等式约束 $\to$ 对偶变量无符号限制
  \item $\ge$ 约束（对 $\min$ 问题）$\to$ 对偶变量 $\le 0$
  \item 自由变量 $\to$ 对偶等式约束
\end{itemize}

\subsection{对偶定理}

\textbf{定理 3.1（弱对偶定理）}
设 $x$ 和 $y$ 分别是 (P) 和 (D) 的可行解，则 $c^T x \ge b^T y$。
推论：若 $c^T x = b^T y$，则 $x$ 和 $y$ 分别是各自问题的最优解。

\textbf{定理 3.2（强对偶定理）}
若 (P) 有有限最优解 $x^*$，则 (D) 也有最优解 $y^*$，且 $c^T x^* = b^T y^*$。

\subsection{互补松弛条件}

\textbf{定理 3.3（互补松弛）}
设 $x^*$ 和 $y^*$ 分别是 (P) 和 (D) 的可行解。它们同时为最优的充要条件是：
\[
(y^*)^T(Ax^* - b) = 0,\qquad (c - A^T y^*)^T x^* = 0
\]
即：
\begin{itemize}
  \item 若 $x_j^* > 0$，则对应对偶约束取等号
  \item 若对偶约束严格不取等，则 $x_j^* = 0$
  \item 若 $y_i^* > 0$，则对应原约束取等号
  \item 若原约束严格不取等，则 $y_i^* = 0$
\end{itemize}

\subsection{对偶单纯形法}

\textbf{适用场景：} 原始不可行但对偶可行（检验数全 $\ge 0$ 但 $B^{-1}b$ 有负分量）。

\textbf{算法步骤：}
\begin{enumerate}
  \item 确定出基变量：选 $B^{-1}b$ 中最负的分量对应行
  \item 确定进基变量：在该行负系数列中，取 $\displaystyle \min\left\{\frac{\sigma_j}{|a_{rj}|} \;\middle|\; a_{rj} < 0\right\}$
  \item 转轴运算（同单纯形法）
  \item 重复直至 $B^{-1}b \ge 0$（原始可行）
\end{enumerate}

\subsection{影子价格}

\textbf{定义：} 对偶变量 $y_i^*$ 的经济含义——第 $i$ 种资源增加 1 单位时，最优目标值的边际变化量。$y_i^* = \frac{\partial z^*}{\partial b_i}$。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{对称对偶}：$\min\ c^Tx,\ Ax\ge b,\ x\ge0 \;\longleftrightarrow\; \max\ b^Ty,\ A^Ty\le c,\ y\ge0$
  \item \textbf{弱对偶}：$c^Tx \ge b^Ty$；\textbf{强对偶}：最优值相等
  \item \textbf{互补松弛}：$(y^*)^T(Ax^*-b)=0$，$(c-A^Ty^*)^T x^*=0$
  \item \textbf{对偶单纯形法}：原始不可行但对偶可行时使用
  \item \textbf{影子价格}：$y_i^* = \partial z^* / \partial b_i$
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch03.tex
git commit -m "feat: notes-ch03 对偶理论"
```

---

### Task 5: 创建 `notes-ch04.tex` — 灵敏度分析

**Files:**
- Read: `latex/review/review-ch04.tex`
- Create: `latex/notes/notes-ch04.tex`

- [ ] **Step 1: 从 review-ch04.tex 提取纯方法内容**

提取灵敏度分析的四种情况公式：c变化（基变量/非基变量）、b变化、新增约束、新增变量。删除自编例题和真题。

```latex
% ============================================================
%  第4章：灵敏度分析
% ============================================================
\section{第4章 \quad 灵敏度分析}

\subsection{目标系数 $c$ 的变化}

\textbf{非基变量 $c_j$ 变化：}
仅影响对应检验数 $\sigma_j = c_j - c_B^T B^{-1}a_j$。
若 $\sigma_j$ 仍 $\ge 0$（$\min$ 问题），原最优解不变。
变化范围：$c_j \le c_B^T B^{-1}a_j$。

\textbf{基变量 $c_B$ 变化：}
影响所有非基变量检验数。需重新计算 $\sigma_N = c_N - (c_B + \Delta c_B)B^{-1}N$。
若全部 $\ge 0$，原最优解不变。

\subsection{右端常数 $b$ 的变化}

$b \to b + \Delta b$ 后，基变量取值变为 $x_B = B^{-1}(b + \Delta b)$。
若 $B^{-1}(b + \Delta b) \ge 0$，则当前基仍可行且最优（目标值变为 $c_B^T B^{-1}(b+\Delta b)$）。
若出现负分量，需用对偶单纯形法恢复可行性。

\subsection{新增约束}

在原最优表基础上添加新约束行。若原最优解满足新约束，则仍为最优。
否则添加松弛/人工变量，用对偶单纯形法继续迭代。

\subsection{新增变量}

计算新变量的检验数 $\sigma_{n+1} = c_{n+1} - c_B^T B^{-1}a_{n+1}$。
若 $\sigma_{n+1} \ge 0$（$\min$ 问题），新变量不进基，原解仍最优。
若 $\sigma_{n+1} < 0$，新变量进基，继续迭代。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{非基变量 $c_j$ 变}：只影响自身检验数
  \item \textbf{基变量 $c_B$ 变}：影响全部非基检验数，需重算
  \item \textbf{$b$ 变}：基变量取值变 $B^{-1}(b+\Delta b)$，不可行时用对偶单纯形
  \item \textbf{新增约束}：加入原最优表，必要时对偶单纯形
  \item \textbf{新增变量}：算检验数，负则进基
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch04.tex
git commit -m "feat: notes-ch04 灵敏度分析"
```

---

### Task 6: 创建 `notes-ch05.tex` — 凸集与凸函数

**Files:**
- Read: `latex/review/review-ch05.tex`
- Create: `latex/notes/notes-ch05.tex`

- [ ] **Step 1: 从 review-ch05.tex 提取纯方法内容**

提取凸集定义、凸函数定义及判别法（一阶/二阶/Hessian）、凸规划性质、3层判别法递进。删除自编例题。

```latex
% ============================================================
%  第5章：凸集与凸函数
% ============================================================
\section{第5章 \quad 凸集与凸函数}

\subsection{凸集}

\textbf{定义 5.1（凸集）}
集合 $C \subseteq \mathbb{R}^n$ 称为凸集，若对任意 $x,y \in C$ 和 $\lambda \in [0,1]$，有 $\lambda x + (1-\lambda)y \in C$。

\textbf{常见凸集：} 多面体 $\{x\mid Ax\le b\}$、单位圆盘、半空间 $\{x\mid a^Tx\le b\}$、LP可行域 $\{x\mid Ax=b,\ x\ge 0\}$。

\textbf{反例：} 圆环（有洞）、坐标轴十字（不实心）、整数点集（不连通）。

（课件 p3.1, p3.2）

\subsection{凸函数}

\textbf{定义 5.2（凸函数）}
函数 $f: C\to\mathbb{R}$（$C$ 为凸集）称为凸函数，若对任意 $x,y\in C$ 和 $\lambda\in[0,1]$：
\[
f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda) f(y)
\]

\subsection{凸函数的判别——三层递进}

\textbf{第1层：一阶条件（对可微函数）}
$f$ 凸 $\Longleftrightarrow$ $f(y) \ge f(x) + \nabla f(x)^T(y-x)$，$\forall x,y$。
几何：函数图像在任一点切线上方。

\textbf{第2层：二阶条件（对二次可微函数）}
$f$ 凸 $\Longleftrightarrow$ $\nabla^2 f(x) \succeq 0$（半正定），$\forall x$。
若 $\nabla^2 f(x) \succ 0$（正定），则 $f$ 严格凸。

\textbf{第3层：Hessian 正定性判别}
\begin{itemize}
  \item 顺序主子式法：所有顺序主子式 $>0$ $\Rightarrow$ 正定
  \item 特征值法：所有特征值 $>0$ $\Rightarrow$ 正定
  \item 对 $2\times 2$ 矩阵：$a_{11}>0$ 且 $\det>0$ $\Rightarrow$ 正定
\end{itemize}

\subsection{凸规划}

\textbf{定义：} $\min\{f(x)\mid g_i(x)\le 0,\ h_j(x)=0\}$ 中，若 $f$ 凸，$g_i$ 凸（$\le 0$ 约束），$h_j$ 仿射（$=0$ 约束），则为凸规划。

\textbf{定理 5.X（凸规划的最优性）}
凸规划的局部极小点必为全局极小点。若 $f$ 严格凸，则最优解唯一。
此外，若 Slater 条件成立，KKT 点即为全局最优解。

\textbf{核心逻辑链：}
凸集 $\to$ 凸函数 $\to$ 凸规划 $\to$ 局部极小=全局极小 $\to$ KKT充要。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{凸集判别}：实心、无洞、无凹坑
  \item \textbf{凸函数判别（三层）}：一阶梯度不等式 $\to$ 二阶 Hessian 半正定 $\to$ 主子式/特征值
  \item \textbf{凸规划}：$f$ 凸 + $g_i$ 凸 + $h_j$ 仿射 $\to$ 局部=全局
  \item \textbf{严格凸}：Hessian 正定 $\to$ 最优解唯一
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch05.tex
git commit -m "feat: notes-ch05 凸集与凸函数"
```

---

### Task 7: 创建 `notes-ch06.tex` — 最优性条件（FJ与KKT）

**Files:**
- Read: `latex/review/review-ch06.tex`
- Create: `latex/notes/notes-ch06.tex`

- [ ] **Step 1: 从 review-ch06.tex 提取纯方法内容**

提取无约束条件、Lagrange乘子法、FJ条件（完整方程组+λ₀讨论）、KKT条件、约束规格定义、FJ vs KKT对比表。删除所有自编例题和真题。

```latex
% ============================================================
%  第6章：最优性条件（FJ与KKT）
% ============================================================
\section{第6章 \quad 最优性条件（FJ与KKT）}

\subsection{无约束极值条件}

\textbf{一阶必要条件：} 若 $x^*$ 局部极小且 $f$ 可微，则 $\nabla f(x^*) = 0$。

\textbf{二阶必要条件：} 若 $f$ 二次可微，则 $\nabla f(x^*)=0$ 且 $\nabla^2 f(x^*)$ 半正定。

\textbf{二阶充分条件：} 若 $\nabla f(x^*)=0$ 且 $\nabla^2 f(x^*)$ 正定，则 $x^*$ 严格局部极小。

\subsection{Lagrange乘子法（仅等式约束）}

考虑 $\min f(x)$ s.t. $h_i(x)=0$。Lagrange函数 $L(x,\mu)=f(x)+\sum\mu_i h_i(x)$。
若 $x^*$ 局部极小且 $\nabla h_i(x^*)$ 线性无关，则存在乘子使 $\nabla_x L(x^*,\mu^*)=0$。
几何：$-\nabla f(x^*)$ 落在约束法向量张成的子空间中。

\subsection{FJ条件（Fritz John, 1948）}

\textbf{定理 6.2（FJ条件）}
对一般约束问题 $\min f(x)$ s.t. $g_i(x)\le 0$，$h_j(x)=0$。若 $x^*$ 局部极小且函数连续可微，则存在{\color{red}不全为零}的乘子 $\lambda_0,\lambda_1,\dots,\lambda_m,\mu_1,\dots,\mu_p$：
\[
\boxed{\lambda_0 \nabla f(x^*) + \sum_{i=1}^m \lambda_i \nabla g_i(x^*) + \sum_{j=1}^p \mu_j \nabla h_j(x^*) = 0}
\]
\[
\lambda_i \ge 0\ (i=0,1,\dots,m),\qquad \lambda_i g_i(x^*) = 0\ (i=1,\dots,m)
\]
$\mu_j$ 无符号约束。

\textbf{注意 $\lambda_0$ 的特殊性：} $\lambda_0$ 可为 $0$——此时目标梯度完全消失，FJ退化为仅约束梯度的线性相关。这是FJ条件的"软肋"，也是引入约束规格的动机。

（课件 p7.17, p7.26）

\subsection{KKT条件}

\textbf{定理 6.3（KKT条件）}
在FJ基础上{\color{red}加上约束规格}，强制 $\lambda_0 \neq 0$，归一化 $\lambda_0=1$：
\[
\nabla f(x^*) + \sum_{i=1}^m \lambda_i \nabla g_i(x^*) + \sum_{j=1}^p \mu_j \nabla h_j(x^*) = 0
\]
加上：$g_i(x^*)\le 0$，$h_j(x^*)=0$，$\lambda_i\ge 0$，$\lambda_i g_i(x^*)=0$。

Lagrange函数 $L(x,\lambda,\mu)=f(x)+\sum\lambda_i g_i(x)+\sum\mu_j h_j(x)$。
则条件等价于 $\nabla_x L=0$ + $\lambda_i g_i=0$。

（课件 p7.19, p7.20, p7.27）

\subsection{约束规格（CQ）}

\textbf{作用：} 保证约束梯度的线性化与真实可行域局部几何一致，使KKT必要条件成立。

\textbf{常用约束规格：}
\begin{itemize}
  \item \textbf{LICQ}：积极约束梯度线性无关（最强，验证简单）
  \item \textbf{MFCQ}：积极约束梯度正线性相关（较LICQ稍弱）
  \item \textbf{Slater}：凸问题中存在严格可行点 $g_i(x)<0$
  \item \textbf{线性约束}：CQ自动成立，无需验证
\end{itemize}

\subsection{FJ vs KKT 对比}

\begin{tabular}{@{}p{18mm}@{}p{35mm}@{}p{35mm}@{}}
\toprule
& \textbf{FJ} & \textbf{KKT} \\
\midrule
$\lambda_0$ & $\ge0$，可为0 & 归一化 $=1$ \\
\midrule
是否需要CQ & 不需要 & 必须 \\
\midrule
适用范围 & 所有局部极小点 & 仅满足CQ的局部极小点 \\
\midrule
$\lambda_0=0$时 & 目标梯度消失 & 不存在此退化 \\
\midrule
解题方法 & 分$\lambda_0=0$和$\lambda_0\neq0$讨论 & 分互补松弛情形讨论 \\
\bottomrule
\end{tabular}

\subsection{本章速查}

\begin{itemize}
  \item \textbf{FJ}：$\lambda_0\nabla f + \sum\lambda_i\nabla g_i + \sum\mu_j\nabla h_j = 0$，$\lambda_0,\lambda_i\ge0$，$\lambda_i g_i=0$，乘子不全为零
  \item \textbf{KKT}：同上但 $\lambda_0=1$，需要CQ
  \item \textbf{核心区别}：FJ允许$\lambda_0=0$，KKT不允许
  \item \textbf{LICQ}：积极约束梯度线性无关——最常用
  \item \textbf{FJ解题}：分$\lambda_0=0$和$\lambda_0\neq0$；\textbf{KKT解题}：分互补松弛情形
  \item \textbf{退化判断}：检查积极约束梯度是否为零向量
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch06.tex
git commit -m "feat: notes-ch06 最优性条件（FJ与KKT）"
```

---

### Task 8: 创建 `notes-ch07.tex` — 非线性对偶

**Files:**
- Read: `latex/review/review-ch07.tex`
- Create: `latex/notes/notes-ch07.tex`

- [ ] **Step 1: 从 review-ch07.tex 提取纯方法内容**

提取Lagrange对偶定义、对偶函数、弱/强对偶定理、鞍点与KKT关系、Wolfe对偶。删除自编例题。

```latex
% ============================================================
%  第7章：非线性对偶
% ============================================================
\section{第7章 \quad 非线性对偶}

\subsection{Lagrange对偶}

\textbf{原问题 (P)：}
$\min\ f(x)$ s.t. $g_i(x)\le 0$，$h_j(x)=0$。

\textbf{Lagrange函数：}
$L(x,\lambda,\mu) = f(x) + \sum_{i=1}^m \lambda_i g_i(x) + \sum_{j=1}^p \mu_j h_j(x)$，$\lambda_i \ge 0$。

\textbf{对偶函数：}
$\theta(\lambda,\mu) = \inf_{x}\ L(x,\lambda,\mu)$。对偶函数对任意 $\lambda\ge 0$ 给出原问题最优值的下界。

\textbf{对偶问题 (D)：}
$\max\ \theta(\lambda,\mu)$ s.t. $\lambda \ge 0$。

\subsection{对偶定理}

\textbf{定理 7.1（弱对偶）}
对任意原可行解 $x$ 和 $\lambda\ge 0$：$\theta(\lambda,\mu) \le f(x)$。即对偶最优值 $\le$ 原最优值。

\textbf{定理 7.2（强对偶）}
若 (P) 为凸规划且 Slater 条件成立，则 $\theta^* = f^*$，且对偶最优解可达。

\textbf{对偶间隙：} $f^* - \theta^* \ge 0$。非凸问题中可能 $>0$。

\subsection{鞍点与KKT}

\textbf{定义（鞍点）}
$(\bar{x},\bar{\lambda},\bar{\mu})$（$\bar{\lambda}\ge 0$）称为 $L$ 的鞍点，若
$L(\bar{x},\lambda,\mu) \le L(\bar{x},\bar{\lambda},\bar{\mu}) \le L(x,\bar{\lambda},\bar{\mu})$，$\forall x,\lambda\ge 0,\mu$。
即 $\bar{x}$ 极小化 $L(\cdot,\bar{\lambda},\bar{\mu})$，$(\bar{\lambda},\bar{\mu})$ 极大化 $L(\bar{x},\cdot,\cdot)$。

\textbf{定理：} 鞍点存在 $\Longleftrightarrow$ 强对偶成立且原/对偶最优解可达。

\subsection{Wolfe对偶（二次规划）}

对二次规划 $\min\ \frac{1}{2}x^TQx + c^Tx$ s.t. $Ax\le b$（$Q\succ 0$）：
Wolfe对偶为 $\max\ -\frac{1}{2}y^TQy + b^T\lambda$ s.t. $Qy + c + A^T\lambda = 0$，$\lambda\ge 0$。
最优解满足 $x^* = y^*$。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{对偶函数}：$\theta(\lambda,\mu) = \inf_x L(x,\lambda,\mu)$
  \item \textbf{弱对偶}：$\theta^* \le f^*$；\textbf{强对偶}：凸+Slater $\Rightarrow \theta^* = f^*$
  \item \textbf{对偶间隙}：$f^* - \theta^*$，非凸时可 $>0$
  \item \textbf{鞍点}：$\Longleftrightarrow$ 强对偶成立且解可达
  \item \textbf{Wolfe对偶}：二次规划的特化对偶形式
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch07.tex
git commit -m "feat: notes-ch07 非线性对偶"
```

---

### Task 9: 创建 `notes-ch08.tex` — 无约束优化方法

**Files:**
- Read: `latex/review/review-ch08.tex`
- Create: `latex/notes/notes-ch08.tex`

- [ ] **Step 1: 从 review-ch08.tex 提取纯方法内容**

提取下降算法框架、最速下降法、牛顿法、共轭梯度法、DFP/BFGS公式、Armijo准则。删除自编教学例和真题。

```latex
% ============================================================
%  第8章：无约束优化方法
% ============================================================
\section{第8章 \quad 无约束优化方法}

\subsection{下降算法通用框架}

\textbf{迭代格式：} $x^{(k+1)} = x^{(k)} + \lambda_k d^{(k)}$
\begin{itemize}
  \item $d^{(k)}$：搜索方向，满足 $\nabla f(x^{(k)})^T d^{(k)} < 0$
  \item $\lambda_k > 0$：步长，使 $f(x^{(k+1)}) < f(x^{(k)})$
  \item 终止：$\|\nabla f(x^{(k)})\| \le \varepsilon$
\end{itemize}
（课件 p10.1）

\subsection{最速下降法}

\textbf{方向：} $d^{(k)} = -\nabla f(x^{(k)})$（负梯度，局部下降最快）。

\textbf{锯齿现象：} 精确线搜索下 $d^{(k)} \perp d^{(k+1)}$。Hessian条件数大时严重，收敛慢。

\subsection{牛顿法}

\textbf{方向：} $d^{(k)} = -[\nabla^2 f(x^{(k)})]^{-1} \nabla f(x^{(k)})$，步长 $\lambda_k = 1$。

\textbf{二次收敛：} $\|x^{(k+1)}-x^*\| \le C\|x^{(k)}-x^*\|^2$。对正定二次函数一步收敛。
代价：需算 Hessian 逆 $O(n^3)$。

\subsection{线搜索（步长确定）}

\textbf{精确线搜索：} 解 $\phi'(\lambda)=0$ 得 $\lambda_k = \operatorname{argmin}_{\lambda\ge 0} f(x+\lambda d)$。

\textbf{Armijo准则（非精确）：}
从 $\lambda=1$ 开始回溯（缩半 $\beta\in(0,1)$），直至：
$f(x+\lambda d) \le f(x) + \alpha\lambda \nabla f(x)^T d$，
其中 $\alpha\in(0,1)$（常取 $10^{-4}$），$\beta$ 常取 $0.5$。

（课件 p9.8, p9.9）

\subsection{FR共轭梯度法}

\textbf{方向：}
$\beta_k = \frac{\|\nabla f^{(k)}\|^2}{\|\nabla f^{(k-1)}\|^2}$，
$d^{(k)} = -\nabla f^{(k)} + \beta_k d^{(k-1)}$
（初始 $d^{(0)} = -\nabla f^{(0)}$）。

\textbf{性质：} $O(n)$ 存储，对正定二次函数至多 $n$ 步收敛。方向满足 $(d^{(i)})^T Q d^{(j)} = 0$（$Q$-共轭）。

（课件 p10.7）

\subsection{拟牛顿法}

\textbf{拟牛顿条件（割线方程）：}
$s_{k-1} = x^{(k)} - x^{(k-1)}$，$y_{k-1} = \nabla f^{(k)} - \nabla f^{(k-1)}$。
$H_k y_{k-1} = s_{k-1}$（$H_k \approx [\nabla^2 f]^{-1}$）。

\textbf{DFP公式（校 $H$ = Hessian逆近似）：}
\[
H_k = H_{k-1}
    + \frac{s_{k-1}s_{k-1}^T}{s_{k-1}^T y_{k-1}}
    - \frac{H_{k-1}y_{k-1}y_{k-1}^T H_{k-1}}{y_{k-1}^T H_{k-1} y_{k-1}}
\]
搜索方向：$d^{(k)} = -H_k \nabla f^{(k)}$。初始化 $H_0 = I$。

\textbf{BFGS公式（校 $B$ = Hessian近似）：}
\[
B_k = B_{k-1}
    + \frac{y_{k-1}y_{k-1}^T}{y_{k-1}^T s_{k-1}}
    - \frac{B_{k-1}s_{k-1}s_{k-1}^T B_{k-1}}{s_{k-1}^T B_{k-1} s_{k-1}}
\]
拟牛顿条件：$B_k s_{k-1} = y_{k-1}$。搜索方向：解 $B_k d^{(k)} = -\nabla f^{(k)}$。

\textbf{DFP vs BFGS：} DFP校 $H$（逆），BFGS校 $B$（Hessian本身）。公式对称（$s \leftrightarrow y$互换）。考试以DFP为主。

\textbf{二次终止性：} DFP/BFGS/共轭梯度对正定二次函数至多 $n$ 步收敛，产生的方向关于 $Q$ 共轭。

（课件 p10.52--p10.63）

\subsection{本章速查}

\begin{itemize}
  \item \textbf{最速下降}：$d = -\nabla f$，锯齿正交，收敛慢
  \item \textbf{牛顿法}：$d = -H^{-1}\nabla f$，二次收敛，$O(n^3)$贵
  \item \textbf{精确线搜索}：解 $\phi'(\lambda)=0$；\textbf{Armijo}：回溯缩步
  \item \textbf{FR共轭梯度}：$\beta_k = \|\nabla f^{(k)}\|^2 / \|\nabla f^{(k-1)}\|^2$，$O(n)$存储，$n$步收敛
  \item \textbf{DFP}：$H_k = H_{k-1} + \frac{ss^T}{s^Ty} - \frac{Hyy^TH}{y^THy}$（校Hessian逆）
  \item \textbf{BFGS}：$B_k = B_{k-1} + \frac{yy^T}{y^Ts} - \frac{Bss^TB}{s^TBs}$（校Hessian本身）
  \item \textbf{拟牛顿条件}：$H_k y_{k-1} = s_{k-1}$（DFP）/ $B_k s_{k-1} = y_{k-1}$（BFGS）
  \item \textbf{二次终止性}：对正定二次函数至多$n$步收敛
  \item \textbf{遗传正定性}：$s^Ty > 0$时DFP/BFGS保持矩阵正定性
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch08.tex
git commit -m "feat: notes-ch08 无约束优化方法"
```

---

### Task 10: 创建 `notes-ch09.tex` — 约束优化方法

**Files:**
- Read: `latex/review/review-ch09.tex`
- Create: `latex/notes/notes-ch09.tex`

- [ ] **Step 1: 从 review-ch09.tex 提取纯方法内容**

提取可行方向法框架、Zoutendijk法、Rosen梯度投影法、罚函数法（外点/内点/乘子法）。删除自编例题和真题。

```latex
% ============================================================
%  第9章：约束优化方法
% ============================================================
\section{第9章 \quad 约束优化方法}

\subsection{两大流派}

\begin{itemize}
  \item \textbf{可行方向法}：始终在可行域内，每步找下降可行方向。代表：Zoutendijk、Rosen梯度投影。
  \item \textbf{罚函数法}：转化为一系列无约束子问题，逐轮加大惩罚。代表：外点法（SUMT）、内点法（障碍法）、乘子法。
\end{itemize}

（课件 p12.1, p12.2）

\subsection{可行方向法通用框架}

\begin{enumerate}
  \item 初始可行点 $x^{(0)}$，$k=0$
  \item 确定积极约束集 $I_k$（当前取等号的不等式约束）
  \item 求解子问题得下降可行方向 $d^{(k)}$
  \item 沿 $d^{(k)}$ 一维搜索，保持可行性
  \item $x^{(k+1)} = x^{(k)} + \lambda_k d^{(k)}$
  \item 满足KKT则停止，否则 $k\leftarrow k+1$ 回第2步
\end{enumerate}

\textbf{可行方向条件：}
\begin{itemize}
  \item 积极不等式约束：$\nabla g_i(x)^T d \le 0$（不指向域外）
  \item 等式约束：$\nabla h_j(x)^T d = 0$（沿切向）
  \item 非积极约束：局部可忽略
\end{itemize}

\subsection{Rosen梯度投影法}

\textbf{投影矩阵（线性约束）：}
$P = I - M^T(MM^T)^{-1}M$，
其中 $M$ 为积极约束系数矩阵（每行一个 $\nabla g_i^T$）。

\textbf{搜索方向：} $d = -P\nabla f$（负梯度在切空间上的正交投影）。

\textbf{算法步骤：}
\begin{enumerate}
  \item 识别当前积极约束，构造 $M$
  \item 计算 $P = I - M^T(MM^T)^{-1}M$
  \item $d = -P\nabla f(x)$
  \item 若 $d \neq 0$：沿 $d$ 线搜索，更新 $x$，回到1
  \item 若 $d = 0$：计算 $w = -(MM^T)^{-1}M\nabla f(x)$
  \begin{itemize}
    \item 若 $w$ 全 $\ge 0$ $\to$ KKT点，停止
    \item 若 $w$ 有负分量 $\to$ 去掉对应约束行，重新计算 $P$
  \end{itemize}
\end{enumerate}

\subsection{Zoutendijk法}

解LP子问题求下降可行方向：
\[
\min\ \nabla f(x)^T d,\quad
\text{s.t.}\ \nabla g_i(x)^T d + g_i(x) \le 0,\quad -1 \le d_j \le 1
\]
最优值 $< 0$ $\Rightarrow$ 得下降可行方向；$= 0$ $\Rightarrow$ FJ/KKT点。

\subsection{罚函数法}

\textbf{外点法（外罚函数）：}
$\min\ P(x,\sigma) = f(x) + \sigma\sum[\max(0,g_i(x))]^2 + \sigma\sum h_j(x)^2$。
$\sigma_k \to \infty$ 逐轮增大惩罚，无约束子问题的解趋向原约束解。

\textbf{内点法（障碍法，$\le$ 约束）：}
$\min\ B(x,r) = f(x) - r\sum\ln(-g_i(x))$ 或 $f(x) + r\sum 1/(-g_i(x))$。
$r_k \to 0$，从可行域内部逼近边界。

\textbf{乘子法（增广Lagrange）：}
外罚函数 + Lagrange乘子项的混合，惩罚力度不需要 $\to\infty$，避免病态。
$\min\ L_A(x,\lambda,\sigma) = f(x) + \sum\lambda_i g_i(x) + \frac{\sigma}{2}\sum g_i(x)^2$。

\subsection{本章速查}

\begin{itemize}
  \item \textbf{可行方向法}：$d$ 满足 $\nabla f^T d < 0$ 且 $\nabla g_i^T d \le 0$（积极约束）
  \item \textbf{Rosen投影}：$P = I - M^T(MM^T)^{-1}M$，$d = -P\nabla f$。$d=0$时计算$w$判断KKT
  \item \textbf{Zoutendijk}：解LP子问题求方向
  \item \textbf{外点法}：加惩罚项，$\sigma_k\to\infty$，从域外逼近
  \item \textbf{内点法}：障碍项，$r_k\to 0$，从域内逼近
  \item \textbf{乘子法}：外罚+乘子混合，$\sigma$无需$\to\infty$
\end{itemize}
```

- [ ] **Step 2: 提交**

```bash
git add latex/notes/notes-ch09.tex
git commit -m "feat: notes-ch09 约束优化方法"
```

---

### Task 11: 更新 Makefile

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: 新增 `make notes-print` target + 扩展 `make clean`**

在 `Makefile` 的 `.PHONY` 行末尾追加 `notes-print`：

```makefile
.PHONY: all slides slides-print slides-reader review-reader notes-print generate extract-exam push push-slides push-review clean
```

在 `review-reader` target 之后、`generate` target 之前加入：

```makefile
# === 考场课堂笔记（A4 打印版）===
notes-print: latex/notes-print.pdf

NOTES_SRCS := $(wildcard latex/review/review-ch*.tex)
latex/notes-print.pdf: latex/notes/notes-print.tex $(NOTES_SRCS)
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex
	cd latex && xelatex -interaction=nonstopmode notes/notes-print.tex
```

在 `clean` target 中追加：

```makefile
	rm -f latex/notes/*.aux latex/notes/*.log latex/notes/*.out latex/notes/*.toc
```

- [ ] **Step 2: 提交**

```bash
git add Makefile
git commit -m "build: 新增 make notes-print target（考场课堂笔记）"
```

---

### Task 12: 编译 + 检查 Overfull 警告

**Files:**
- 编译: `make notes-print`
- 日志: `latex/notes-print.log`

- [ ] **Step 1: 首次编译**

```bash
make notes-print
```

- [ ] **Step 2: 检查 Overfull/Underfull 警告**

```bash
grep -n "Overfull\|Underfull" latex/notes-print.log
```

双栏排版下长公式容易溢出。若有 Overfull hbox，修复策略（按优先级）：
1. 公式换行（`multline` 或 `align` 拆分）
2. 缩小表格列间距（`\tabcolsep`）
3. 绝对不用 `\small` 缩小字号

- [ ] **Step 3: 若需修复，二次编译后确认零警告**

```bash
make notes-print
grep -c "Overfull" latex/notes-print.log  # 预期: 0
```

- [ ] **Step 4: 提交**

```bash
git add latex/notes/ latex/notes-print.pdf
git commit -m "fix: notes-print 编译通过，修复Overfull警告"
```

---

### Task 13: 更新 CLAUDE.md

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: 在 CLAUDE.md 中新增 notes-print 章节**

在"复习材料架构"段落之后、"考试重点"段落之前，插入以下内容：

```markdown
### 考场课堂笔记（notes-print）

`latex/notes/` 目录存放考场用的 A4 课堂笔记，由 `make notes-print` 编译输出 `latex/notes-print.pdf`。

**用途**：开卷考试带入考场，作为"课堂笔记"使用。

**内容边界（硬规则）**：
| ✅ 保留 | ❌ 删除 |
|---------|---------|
| 定义、定理陈述（不证） | 所有证明（含"证明直觉"） |
| 算法步骤（enumerate 枚举） | 所有数字例题（自编例 + 真题） |
| 核心公式 | TikZ 几何图 |
| 方法对比表 | 因果解释段落 |
| PPT 页码引用（行内小字） | defbox/notebox/examquestion 环境 |

**判断原则**：内容只回答"是什么"（定义、定理、公式、步骤），不回答"为什么"（证明、推导）和"怎么用"（例题、真题）。

**与 review 的关系**：
- `notes-chXX.tex` 是 `review-chXX.tex` 的严格子集——只删不增
- **修改 review 某章后，必须同步检查对应 notes 章是否需要更新**
- 编译：`make notes-print`（纳入 `make all`）
```

- [ ] **Step 2: 提交**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: CLAUDE.md 新增 notes-print 章节说明"
```

---

## 依赖关系

```
Task 1 (主入口) ─────────────────────────────────────────────┐
Task 2 (ch01) ─┤                                            │
Task 3 (ch02) ─┤                                            │
Task 4 (ch03) ─┤                                            │
Task 5 (ch04) ─┼── 全部并行（互不依赖） ──▶ Task 12 (编译) ──▶ Task 13 (CLAUDE.md)
Task 6 (ch05) ─┤                                            │
Task 7 (ch06) ─┤                                            │
Task 8 (ch07) ─┤                                            │
Task 9 (ch08) ─┤                                            │
Task 10 (ch09) ─┘                                           │
Task 11 (Makefile) ─────────────────────────────────────────┘
```

- Task 1-11 全部并行（各章文件独立，Makefile修改独立）
- Task 12 必须在 1-11 全部完成后执行（所有文件到位才能编译）
- Task 13 最后执行
