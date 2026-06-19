"""根据 filter_config.json 生成 chapters-reader.tex（阅读器版，2张/页）"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 用户笔记（阅读器版）
NOTES = {
    "7最优性条件": r"""\leafnotepage{
  \section*{FJ vs KKT 条件对比}

  \textbf{FJ条件}：存在不全为零的 $\lambda_0,\dots,\lambda_m,\mu_1,\dots,\mu_l$ 使得
  $\lambda_0\nabla f + \sum\lambda_i\nabla g_i + \sum\mu_j\nabla h_j = 0$，
  $\lambda_i \ge 0$，$\lambda_i g_i = 0$。
  注意：$\lambda_0$ 可以为 0，此时不含目标函数信息。

  \textbf{KKT条件}：增加约束规格后，保证 $\lambda_0 \neq 0$（可归一化为1）。
  $\nabla f + \sum\lambda_i\nabla g_i + \sum\mu_j\nabla h_j = 0$，
  $\lambda_i \ge 0$，$\lambda_i g_i = 0$。
  即 Lagrange 函数 $L(x,\lambda,\mu)$ 的驻点条件。

  真题链接：2025 Q6 — 先求所有FJ点，再证不存在KKT点。
}""",
    "10使用导数的优化算法": r"""\leafnotepage{
  \section*{拟牛顿法公式速查}

  \textbf{DFP（校Hessian逆$H$）}：
  $s_k = x_{k+1}-x_k,\ y_k = g_{k+1}-g_k$
  $H_{k+1} = H_k + \frac{s_k s_k^T}{s_k^T y_k} - \frac{H_k y_k y_k^T H_k}{y_k^T H_k y_k}$
  搜索方向：$d_k = -H_k\nabla f(x_k)$

  \textbf{BFGS（校Hessian $B$）}：
  $B_{k+1} = B_k + \frac{y_k y_k^T}{y_k^T s_k} - \frac{B_k s_k s_k^T B_k}{s_k^T B_k s_k}$
  搜索方向：解 $B_k d_k = -\nabla f(x_k)$

  真题链接：2025 Q4 — DFP法完整两轮迭代。
}""",
    "12可行方向法": r"""\leafnotepage{
  \section*{Rosen梯度投影法}

  投影矩阵：$P = I - M^T(MM^T)^{-1}M$，方向：$d = -P\,\nabla f(x)$

  \textbf{步骤}：
  1. 识别积极约束 → 构造矩阵 $M$
  2. $P = I - M^T(MM^T)^{-1}M$
  3. $d = -P\nabla f(x)$
  4. 若 $d \neq 0$：一维搜索；若 $d=0$：计算
     $w = -(MM^T)^{-1}M\nabla f(x)$
     所有 $w_i \ge 0 \to$ KKT点
     有负分量 $\to$ 去掉对应约束行重算

  \textbf{Zoutendijk法}：解LP子问题 $\min \nabla f^T d$，
  s.t. $\nabla g_i^T d + g_i \le 0$，$-1 \le d_j \le 1$
  最优值$<0$得下降方向；$=0$为FJ/KKT点。

  真题链接：2025 Q5。
}""",
}


def generate():
    with open(os.path.join(SCRIPT_DIR, "filter_config.json"), "r", encoding="utf-8") as f:
        config = json.load(f)

    chapters = [
        ("1引言", "引言"), ("2数学基础", "数学基础"), ("3凸分析", "凸分析"),
        ("4线性规划基本性质", "线性规划基本性质"), ("5单纯形方法", "单纯形方法"),
        ("6对偶理论", "对偶理论"), ("7最优性条件", "最优性条件"), ("8算法", "算法"),
        ("9一维搜索", "一维搜索"), ("10使用导数的优化算法", "使用导数的优化算法"),
        ("11无约束优化直接方法", "无约束优化直接方法"), ("12可行方向法", "可行方向法"),
        ("13罚函数法", "罚函数法"),
    ]

    output_path = os.path.join(PROJECT_DIR, "chapters-reader.tex")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("% chapters-reader.tex — Leaf5 阅读器版（每页2张）\n\n")

        for ch_key, ch_name in chapters:
            pages = config.get(ch_key, [])
            f.write(f"\n% ====== {ch_name}（{len(pages)} 页） ======\n\n")
            if not pages:
                f.write("% （本章不考，已全部排除）\n\n")
                continue
            for i in range(0, len(pages), 2):
                p1 = str(pages[i])
                p2 = str(pages[i+1]) if i+1 < len(pages) else "0"
                f.write(f"\\leafslidepair{{{ch_key}}}{{{p1}}}{{{p2}}}\n")
            if ch_key in NOTES:
                f.write(f"\n{NOTES[ch_key]}\n")
            else:
                f.write(f"\n% ── {ch_name} 章末笔记 ──\n\n")

    total = sum(len(v) for v in config.values())
    print(f"已生成: {output_path}")
    print(f"总计: {total} 页幻灯片 → {(total+1)//2} 页 + 笔记")


if __name__ == "__main__":
    generate()
