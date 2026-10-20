"""Chạy toàn bộ thí nghiệm: 3 cách chia dữ liệu x 7 mô hình.

Cách chạy: uv run python src/run_experiments.py
Kết quả ghi vào experiments/exp001/.
"""

import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import ML_FEATURES, ROOT, load_halides
from src.rules import TauRule, TMuRule, TRule

OUT = ROOT / "experiments" / "exp001"
SEEDS = list(range(10))
N_FOLDS = 5
RULE_COLS = ["t", "mu", "tau"]


def make_models(seed: int) -> dict:
    """Trả về {tên: (mô hình, danh sách cột đầu vào)}. Mô hình học máy dùng
    class_weight='balanced' vì số mẫu perovskite / không perovskite lệch nhau."""
    return {
        "Đa số (baseline)": (DummyClassifier(strategy="most_frequent"), ML_FEATURES),
        "Quy tắc t": (TRule(), RULE_COLS),
        "Quy tắc t + μ": (TMuRule(), RULE_COLS),
        "τ (Bartel)": (TauRule(), RULE_COLS),
        "Hồi quy logistic": (
            make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced")),
            ML_FEATURES,
        ),
        "Cây quyết định": (
            DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=seed),
            ML_FEATURES,
        ),
        "Random forest": (
            RandomForestClassifier(
                n_estimators=300, class_weight="balanced", random_state=seed, n_jobs=-1
            ),
            ML_FEATURES,
        ),
    }


def splits(scheme: str, df: pd.DataFrame, seed: int):
    """Sinh các cặp (train, test) theo 3 cách chia."""
    if scheme == "Ngẫu nhiên":
        return StratifiedKFold(N_FOLDS, shuffle=True, random_state=seed).split(df, df["y"])
    if scheme == "Theo cation B":
        cv = GroupKFold(N_FOLDS, shuffle=True, random_state=seed)
        return cv.split(df, df["y"], groups=df["B"])
    if scheme == "Theo halide X":
        return LeaveOneGroupOut().split(df, df["y"], groups=df["X"])
    raise ValueError(scheme)


def out_of_fold(model, cols, df, split_iter) -> np.ndarray:
    """Dự đoán cho mỗi mẫu khi mẫu đó nằm trong tập test (không bao giờ thấy lúc train)."""
    pred = np.full(len(df), -1)
    for tr, te in split_iter:
        model.fit(df.iloc[tr][cols], df["y"].iloc[tr])
        pred[te] = model.predict(df.iloc[te][cols])
    assert (pred >= 0).all()
    return pred


def main() -> None:
    df = load_halides()
    OUT.mkdir(parents=True, exist_ok=True)
    rows, per_x = [], []
    for scheme in ["Ngẫu nhiên", "Theo cation B", "Theo halide X"]:
        for seed in SEEDS:
            for name, (model, cols) in make_models(seed).items():
                pred = out_of_fold(model, cols, df, splits(scheme, df, seed))
                rows.append({
                    "scheme": scheme, "seed": seed, "model": name,
                    "accuracy": accuracy_score(df["y"], pred),
                    "balanced_accuracy": balanced_accuracy_score(df["y"], pred),
                })
                for x, g in df.assign(pred=pred).groupby("X"):
                    per_x.append({
                        "scheme": scheme, "seed": seed, "model": name, "X": x,
                        "accuracy": accuracy_score(g["y"], g["pred"]),
                    })

    raw = pd.DataFrame(rows)
    raw.to_csv(OUT / "metrics_raw.csv", index=False)
    pd.DataFrame(per_x).to_csv(OUT / "metrics_per_halide.csv", index=False)
    summary = (
        raw.groupby(["scheme", "model"], sort=False)[["accuracy", "balanced_accuracy"]]
        .agg(["mean", "std"]).round(3)
    )
    summary.to_csv(OUT / "summary.csv")

    # tau ngoài mẫu: chỉ các hợp chất Bartel KHÔNG dùng khi tìm ra tau (is_train = -1)
    held = df[df["is_train"] == -1]
    tau_pred = TauRule().fit(held, held["y"]).predict(held)
    tau_check = {
        "n": len(held),
        "accuracy_out_of_sample": round(accuracy_score(held["y"], tau_pred), 3),
        "accuracy_in_sample": round(accuracy_score(
            df[df["is_train"] == 1]["y"],
            TauRule().predict(df[df["is_train"] == 1])), 3),
    }

    config = {
        "data": "data/raw/TableS1.csv (halide F/Cl/Br/I)", "n_samples": len(df),
        "n_perovskite": int(df["y"].sum()), "features_ml": ML_FEATURES,
        "seeds": SEEDS, "n_folds": N_FOLDS, "tau_check": tau_check,
        "python": platform.python_version(), "sklearn": sklearn.__version__,
    }
    (OUT / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), "utf-8")
    pd.set_option("display.width", 160)
    print(summary)
    print(json.dumps(tau_check, ensure_ascii=False))


if __name__ == "__main__":
    main()
