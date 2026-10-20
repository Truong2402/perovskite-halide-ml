"""Vẽ hình cho báo cáo/slide từ kết quả trong experiments/exp001/.

Cách chạy: uv run python src/plots.py  ->  reports/figures/*.png
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import ML_FEATURES, ROOT, load_halides
from src.rules import T_HIGH, T_LOW, TMuRule

EXP = ROOT / "experiments" / "exp001"
FIG = ROOT / "reports" / "figures"

# Bảng màu đã kiểm định (thứ tự cố định), mực chữ trung tính
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
MODELS = ["Quy tắc t", "Quy tắc t + μ", "τ (Bartel)",
          "Hồi quy logistic", "Cây quyết định", "Random forest"]
SCHEMES = {"Ngẫu nhiên": BLUE, "Theo cation B": ORANGE, "Theo halide X": AQUA}

plt.rcParams.update({
    "font.size": 13, "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "figure.dpi": 150, "savefig.bbox": "tight",
    "figure.facecolor": "white",
})


def fig_t_mu_map(df: pd.DataFrame) -> None:
    """Bản đồ t–μ: mỗi điểm là một hợp chất, hình dạng + màu theo nhãn thực nghiệm."""
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for y, color, marker, label in [(0, ORANGE, "x", "Không perovskite"),
                                    (1, BLUE, "o", "Perovskite")]:
        g = df[df["y"] == y]
        ax.scatter(g["t"], g["mu"], s=46, c=color, marker=marker, linewidths=1.6,
                   edgecolors="white" if marker == "o" else None, label=f"{label} (n={len(g)})")
    mu_min = TMuRule().fit(df, df["y"]).mu_min_
    ax.axvspan(T_LOW, T_HIGH, color=BLUE, alpha=0.06, lw=0)
    for v in (T_LOW, T_HIGH):
        ax.axvline(v, color=MUTED, lw=1.2, ls="--")
    ax.axhline(mu_min, color=MUTED, lw=1.2, ls=":")
    ax.text(T_LOW + 0.005, ax.get_ylim()[1] * 0.98, "vùng t của Goldschmidt",
            color=INK2, fontsize=11, va="top")
    ax.text(ax.get_xlim()[1], mu_min + 0.005, f"μ = {mu_min:.2f}", color=INK2,
            fontsize=11, ha="right", va="bottom")
    ax.set_xlabel("Hệ số dung sai Goldschmidt t")
    ax.set_ylabel("Hệ số bát diện μ = r_B / r_X")
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("207 perovskite halide ABX₃ trên bản đồ t–μ", color=INK, loc="left")
    fig.savefig(FIG / "1_ban_do_t_mu.png")
    plt.close(fig)


def fig_scheme_comparison(summary: pd.DataFrame) -> None:
    """Balanced accuracy (trung bình ± độ lệch chuẩn qua 10 seed) theo mô hình và cách chia."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    width = 0.26
    x = np.arange(len(MODELS))
    for i, (scheme, color) in enumerate(SCHEMES.items()):
        s = summary[summary["scheme"] == scheme].set_index("model").loc[MODELS]
        ax.bar(x + (i - 1) * width, s["mean"], width - 0.03, yerr=s["std"], color=color,
               label=scheme, capsize=3, error_kw={"ecolor": INK2, "lw": 1})
    ax.axhline(0.5, color=MUTED, lw=1.2, ls="--", label="Đoán lớp đa số (0.50)")
    ax.axvline(2.5, color=GRID, lw=1.5)
    ax.text(1, 1.02, "Quy tắc vật lý", ha="center", color=INK2, fontsize=12)
    ax.text(4, 1.02, "Học máy", ha="center", color=INK2, fontsize=12)
    ax.set_xticks(x, [m.replace(" ", "\n", 1) if len(m) > 12 else m for m in MODELS])
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Balanced accuracy")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.14),
              title="Cách chia dữ liệu (train/test)")
    fig.savefig(FIG / "2_so_sanh_cach_chia.png")
    plt.close(fig)


def fig_per_halide(per_x: pd.DataFrame) -> None:
    """Độ chính xác trên từng halide khi halide đó bị giấu khỏi tập huấn luyện."""
    t = (per_x[per_x["scheme"] == "Theo halide X"]
         .groupby(["model", "X"])["accuracy"].mean().unstack("X")
         .loc[MODELS, ["F", "Cl", "Br", "I"]])
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.imshow(t.to_numpy(), cmap="Blues", vmin=0.2, vmax=1.0, aspect="auto")
    for (i, j), v in np.ndenumerate(t.to_numpy()):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=12,
                color="white" if v > 0.75 else INK)
    ax.set_xticks(range(4), ["F⁻", "Cl⁻", "Br⁻", "I⁻"])
    ax.set_yticks(range(len(MODELS)), MODELS)
    ax.set_xlabel("Halide bị giấu khi huấn luyện (tập kiểm tra)")
    ax.spines[:].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Accuracy khi ngoại suy sang halide chưa thấy", color=INK, loc="left")
    fig.savefig(FIG / "3_tung_halide.png")
    plt.close(fig)


def fig_tree(df: pd.DataFrame) -> None:
    """Cây quyết định độ sâu 3 (huấn luyện trên toàn bộ dữ liệu, chỉ để minh hoạ luật)."""
    tree = DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=0)
    tree.fit(df[ML_FEATURES], df["y"])
    fig, ax = plt.subplots(figsize=(14, 6))
    plot_tree(tree, feature_names=ML_FEATURES, class_names=["không", "perovskite"],
              filled=False, impurity=False, proportion=False, fontsize=10, ax=ax)
    fig.savefig(FIG / "4_cay_quyet_dinh.png")
    plt.close(fig)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    df = load_halides()
    raw = pd.read_csv(EXP / "metrics_raw.csv")
    summary = (raw.groupby(["scheme", "model"])["balanced_accuracy"]
               .agg(["mean", "std"]).reset_index())
    fig_t_mu_map(df)
    fig_scheme_comparison(summary)
    fig_per_halide(pd.read_csv(EXP / "metrics_per_halide.csv"))
    fig_tree(df)
    print("Đã lưu hình vào", FIG)


if __name__ == "__main__":
    main()
