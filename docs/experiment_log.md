# Nhật ký thí nghiệm (ghi cả thất bại)

## EXP-000 · 2026-10-20 · Kiểm tra tái lập Bartel
- **Mục đích:** code tính lại t, τ và dự đoán khớp dữ liệu gốc (`tests/test_rules.py`, 4/4 pass).
- **Kết quả:** quy tắc t đúng Cl 50.7%, Br 55.6%, I 32.6% — khớp Bartel (51/56/33%). F 83.3%. τ: 91.3% trên 207 halide.
- **Sự cố:** τ tính lại lệch tối đa 0.12 (LiCoBr3) do bảng làm tròn bán kính Co²⁺. Không ảnh hưởng phân loại (dùng cột tau gốc).

## EXP-001 · 2026-10-20 · Quy tắc vs học máy dưới 3 cách chia dữ liệu
- **Giả thuyết (đặt trước):** H1 t kém với halide; H2 ML ≥ τ khi chia ngẫu nhiên nhưng sụt mạnh hơn quy tắc khi ngoại suy.
- **Dữ liệu & chia:** 207 halide. (1) StratifiedKFold 5 fold; (2) GroupKFold 5 fold theo cation B (27 nguyên tố); (3) Leave-one-halide-out (4 fold). 10 seed (0–9), dự đoán out-of-fold gộp lại rồi tính chỉ số.
- **Mô hình:** đa số; t; t+μ (học ngưỡng μ); τ; logistic; cây quyết định (độ sâu 3); random forest (300 cây). ML dùng class_weight="balanced", đặc trưng rA, rB, rX, nA, t, μ.
- **Kết quả — balanced accuracy, trung bình ± độ lệch chuẩn (10 seed):**

| Mô hình | Ngẫu nhiên | Theo cation B | Theo halide X |
|---|---|---|---|
| Đa số | 0.500 | 0.500 | 0.500 |
| Quy tắc t | 0.650 | 0.650 | 0.650 |
| Quy tắc t + μ | 0.879 ± 0.008 | 0.862 ± 0.010 | 0.855 |
| τ (Bartel) | 0.918 | 0.918 | 0.918 |
| Hồi quy logistic | 0.797 ± 0.007 | 0.779 ± 0.020 | 0.694 |
| Cây quyết định | 0.932 ± 0.012 | 0.903 ± 0.012 | 0.832 |
| Random forest | 0.923 ± 0.010 | 0.914 ± 0.013 | 0.802 ± 0.021 |

- **Accuracy khi giấu F⁻:** RF 0.63, cây 0.71, logistic 0.67, τ 0.92, t+μ 0.83. Các halide khác ML vẫn ≥ 0.91 (trừ logistic).
- **τ ngoài mẫu:** 35 halide Bartel không dùng khi tìm τ → accuracy 0.943 (trong mẫu 0.907). n nhỏ nhưng không thấy dấu hiệu τ chỉ "học thuộc".
- **So với baseline:** mọi mô hình trừ quy tắc t đều vượt xa đa số.
- **Nhận xét:**
  - H1 đúng.
  - H2 đúng một phần. Khi chia ngẫu nhiên, cây/RF ngang τ (chênh ≈ 1 độ lệch chuẩn, theo tiêu chí đặt trước là *chưa phân biệt được*).
  - Theo cation B: ML giảm nhẹ.
  - Theo halide X: ML giảm rõ (0.80–0.83 so với 0.918). Gần như toàn bộ mức giảm đến từ F⁻: rX(F) = 1.33 Å nằm ngoài miền train và F chủ yếu là perovskite, ngược với Cl/Br/I.
  - Quy tắc vật lý không phụ thuộc vào việc "đã thấy" halide nào.
- **Giới hạn:** chỉ 4 nhóm halide; Br 27 mẫu; một bộ bán kính.
- **Thư mục chạy:** experiments/exp001/ (config.json, metrics_raw.csv, metrics_per_halide.csv, summary.csv). Hình: reports/figures/.
