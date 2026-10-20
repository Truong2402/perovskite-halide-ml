"""Đọc dữ liệu gốc và tạo tập con perovskite halide ABX3."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "TableS1.csv"
HALIDES = ["F", "Cl", "Br", "I"]

# Đặc trưng cho mô hình học máy: chỉ dùng thông tin mà quy tắc hình học cũng dùng
# (bán kính ion, số oxi hoá) để so sánh công bằng. nB = 3 - nA nên không đưa vào.
ML_FEATURES = ["rA", "rB", "rX", "nA", "t", "mu"]


def load_halides() -> pd.DataFrame:
    """Trả về 207 hợp chất halide với cột y (1 = perovskite, 0 = không) và mu = rB/rX."""
    df = pd.read_csv(RAW_CSV)
    df = df.rename(columns={"rA (Ang)": "rA", "rB (Ang)": "rB", "rX (Ang)": "rX"})
    df = df[df["X"].isin(HALIDES)].reset_index(drop=True)
    df["y"] = (df["exp_label"] == 1).astype(int)
    df["mu"] = df["rB"] / df["rX"]  # octahedral factor
    return df
