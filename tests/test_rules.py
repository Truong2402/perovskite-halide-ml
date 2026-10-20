"""Kiểm tra code tính lại đúng các giá trị có sẵn trong dữ liệu của Bartel."""

import numpy as np

from src.data import load_halides
from src.rules import TauRule, TRule, bartel_tau, goldschmidt_t


def test_halide_subset_size():
    df = load_halides()
    assert len(df) == 207
    assert df["y"].sum() == 81


def test_t_matches_dataset():
    df = load_halides()
    t = goldschmidt_t(df["rA"], df["rB"], df["rX"])
    assert np.allclose(t, df["t"], atol=0.006)  # bảng làm tròn 2 chữ số


def test_tau_matches_dataset():
    df = load_halides()
    tau = bartel_tau(df["rA"], df["rB"], df["rX"], df["nA"])
    # Bảng làm tròn bán kính (vd. Co2+ 0.745 -> 0.74 Å) nhưng cột tau tính từ giá trị
    # chưa làm tròn, nên lệch tối đa ~0.12 (LiCoBr3). Mô hình dùng cột tau gốc.
    assert np.allclose(tau, df["tau"], atol=0.15)


def test_rules_reproduce_bartel_predictions():
    df = load_halides()
    assert (TRule().fit(df, df["y"]).predict(df) == (df["t_pred"] == 1)).all()
    assert (TauRule().fit(df, df["y"]).predict(df) == (df["tau_pred"] == 1)).all()
