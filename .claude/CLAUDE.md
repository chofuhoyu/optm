# CLAUDE.md — 最优化理论与算法 项目规范

## 核心规则

### Git 提交频率
- **每完成一件事立即提交**，不允许批量提交多个不相关的改动
- 每次提交必须 `git push` 到远程
- 提交信息用中文，描述清楚改了什么

### 文件追踪
- `.pptx` 和 `.pdf` 都纳入 git 追踪（不排除）
- `.gitignore` 仅排除：虚拟环境、Python 缓存、LaTeX 辅助文件、OS 杂文件

### 项目结构
- `material/` — PPTX 源文件 + 由 PPTX 生成的 PDF（1:1 页数对应）
- `extracted/` — 每页幻灯片的文字提取（markdown，可搜索）
- `scripts/` — Python 辅助脚本
- `notes/` — 用户手写的 LaTeX 笔记片段
- `main.tex` / `chapters.tex` — LaTeX 排版主文件

### PPTX 与 PDF 关系
- PDF 一律由 PPTX 通过 PowerPoint COM (`win32com`) 转换生成
- `scripts/pptx_to_pdf.py` 用于批量转换
- 转换后 PPTX 页数必须等于 PDF 页数

### 工作语言
- 所有解释、注释用中文
- git 提交信息用中文
