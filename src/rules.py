"""Các quy tắc hình học (t, t+mu, tau) viết dưới dạng bộ phân loại kiểu scikit-learn.

Nhờ cùng giao diện fit/predict, quy tắc và mô hình học máy được đánh giá trên đúng
các lần chia dữ liệu giống nhau.
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import balanced_accuracy_score

# Ngưỡng của Bartel et al. (2019), Science Advances 5, eaav0693
T_LOW, T_HIGH = 0.825, 1.059
TAU_CUT = 4.18


def goldschmidt_t(rA, rB, rX):
    """Hệ số dung sai Goldschmidt: t = (rA + rX) / (sqrt(2) * (rB + rX))."""
    return (rA + rX) / (np.sqrt(2) * (rB + rX))


def bartel_tau(rA, rB, rX, nA):
    """Hệ số tau của Bartel: tau = rX/rB - nA * (nA - (rA/rB) / ln(rA/rB))."""
    ratio = rA / rB
    return rX / rB - nA * (nA - ratio / np.log(ratio))


class _Rule(BaseEstimator, ClassifierMixin):
    """Lớp cha: quy tắc nhận DataFrame, trả về 1 (perovskite) hoặc 0."""

    def fit(self, X, y):
        self.classes_ = np.array([0, 1])
        return self


class TRule(_Rule):
    """Perovskite nếu 0.825 < t < 1.059. Không học gì từ dữ liệu."""

    def predict(self, X):
        return ((X["t"] > T_LOW) & (X["t"] < T_HIGH)).astype(int).to_numpy()


class TauRule(_Rule):
    """Perovskite nếu tau < 4.18. Không học từ dữ liệu ở đây, nhưng tau đã được
    Bartel tìm ra trên chính bộ dữ liệu này (lợi thế "trong mẫu")."""

    def predict(self, X):
        return (X["tau"] < TAU_CUT).astype(int).to_numpy()


class TMuRule(_Rule):
    """Perovskite nếu t trong khoảng của Bartel VÀ mu > ngưỡng.
    Ngưỡng mu được chọn trên tập train để tối đa balanced accuracy (học 1 tham số)."""

    def fit(self, X, y):
        super().fit(X, y)
        t_ok = (X["t"] > T_LOW) & (X["t"] < T_HIGH)
        best_score, best_thr = -1.0, 0.0
        for thr in np.unique(X["mu"]):
            pred = (t_ok & (X["mu"] > thr)).astype(int)
            score = balanced_accuracy_score(y, pred)
            if score > best_score:
                best_score, best_thr = score, thr
        self.mu_min_ = float(best_thr)
        return self

    def predict(self, X):
        t_ok = (X["t"] > T_LOW) & (X["t"] < T_HIGH)
        return (t_ok & (X["mu"] > self.mu_min_)).astype(int).to_numpy()
