# Kế hoạch nghiên cứu — v1 (2026-10-20)

**Đề tài:** Quy tắc hình học hay học máy? Đánh giá khả năng ngoại suy sang hoá học mới khi dự đoán khả năng hình thành perovskite halide
**Phạm vi:** phương án nhẹ · Môn Nhập môn ngành · **Hạn nộp: 2026-11-03** (14 ngày)

## 1. Câu hỏi nghiên cứu
- **Q1 (tái lập):** Trên dữ liệu thực nghiệm của Bartel và cộng sự (2019), quy tắc t, cặp (t, μ) và hệ số τ phân loại đúng bao nhiêu % perovskite halide?
- **Q2 (điểm mới):** Mô hình học máy đơn giản tốt hơn các quy tắc khi chia dữ liệu ngẫu nhiên. Lợi thế đó còn giữ được không khi gặp **halide (X) hoặc cation B chưa thấy trong tập huấn luyện**?

## 2. Giả thuyết (viết trước khi chạy, không sửa sau)
- H1: t đơn lẻ kém với halide (Bartel báo 33–56%); (t, μ) và τ tốt hơn.
- H2: Khi chia ngẫu nhiên, ML ≥ τ. Khi chia theo nhóm hoá học, độ chính xác của ML giảm rõ hơn so với các quy tắc vật lý.
- Nếu H2 sai (ML vẫn tốt khi ngoại suy), đó vẫn là kết quả có giá trị và phải báo cáo trung thực.

## 3. Dữ liệu
- Nguồn: `TableS1.csv`, kho github.com/CJBartel/perovskite-stability (giấy phép MIT); bài gốc DOI 10.1126/sciadv.aav0693.
- Có sẵn các cột: A, B, X, nA, nB, nX, rA, rB, rX (Å), t, tau, exp_label (+1 là perovskite, −1 là không).
- Tập con: X ∈ {F, Cl, Br, I}, khoảng 207 mẫu (cần kiểm lại). μ = rB / rX (tự tính).
- **Cảnh báo cần nêu trong báo cáo:** τ được tìm (SISSO) trên chính 576 mẫu này. Vì vậy độ chính xác của τ ở đây là "trong mẫu" (in-sample), được lợi thế không công bằng so với ML.

## 4. Phương pháp
| Mô hình | Đầu vào | Có học từ dữ liệu? |
|---|---|---|
| Baseline: luôn đoán lớp chiếm đa số | — | không |
| Quy tắc t: 0.825 < t < 1.059 (ngưỡng của Bartel) | t | không |
| Quy tắc (t, μ): ngưỡng μ học từ tập train | t, μ | có (1 ngưỡng) |
| τ: dùng cột `tau_pred` có sẵn, tính lại để kiểm chứng | τ | không (đã fit sẵn) |
| Hồi quy logistic | rA, rB, rX, nA, nB, t, μ | có |
| Cây quyết định (độ sâu ≤ 3, đọc được luật) | như trên | có |
| Random forest | như trên | có |

**Cách chia dữ liệu:**
1. Ngẫu nhiên phân tầng, 5-fold, lặp 10 lần với 10 seed.
2. **Leave-one-halide-out:** huấn luyện trên 3 halide, kiểm tra trên halide còn lại (4 lần).
3. **Theo nhóm cation B (GroupKFold):** cùng một nguyên tố B không xuất hiện ở cả train lẫn test.

**Chỉ số:** accuracy và balanced accuracy (vì số mẫu hai lớp có thể lệch nhau), ma trận nhầm lẫn. Báo cáo trung bình ± độ lệch chuẩn qua các lần chạy.

## 5. Tiêu chí kết luận (đặt trước)
- "A tốt hơn B" chỉ khi chênh lệch balanced accuracy > 1 độ lệch chuẩn qua các lần chạy. Nếu không thì kết luận "chưa phân biệt được".
- Bước tái lập đạt yêu cầu nếu độ chính xác của t theo từng halide khớp số của Bartel trong khoảng ±3%. Nếu không khớp, phải tìm nguyên nhân trước khi đi tiếp.

## 6. Giới hạn đã biết
Dữ liệu nhỏ (khoảng 200 mẫu, Br chỉ khoảng 27). Chỉ dùng một bộ bán kính ion (Shannon); độ nhạy theo bán kính để làm sau. Nhãn là formability thực nghiệm, không phải ổn định nhiệt động hay độ bền môi trường.

## 7. Lịch 14 ngày
| Ngày | Ngày tháng | Việc | Sản phẩm | Điểm dừng để bạn duyệt |
|---|---|---|---|---|
| 1 | 21/10 | Tải dữ liệu (xin phép), ghi SHA256, lọc halide, điền data_card | `data/raw/TableS1.csv`, `src/data.py` | ✔ |
| 2–3 | 22–23/10 | Khám phá dữ liệu: số mẫu theo X và nhãn, bản đồ t–μ | `notebooks/01_eda.ipynb`, 2 hình | ✔ |
| 4–5 | 24–25/10 | Tái lập t, (t, μ), τ; so với số của Bartel | `src/rules.py`, bảng 1 | ✔ (kiểm chứng tái lập) |
| 6–8 | 26–28/10 | ML với chia ngẫu nhiên, so với baseline | `src/models.py`, `src/evaluate.py`, bảng 2 | ✔ |
| 9–10 | 29–30/10 | Chia theo nhóm (theo X, theo B), so sánh mức sụt giảm | bảng 3, hình chính | ✔ |
| 11 | 31/10 | Chạy lại toàn bộ từ đầu, rà checklist | `experiments/`, log | |
| 12–13 | 1–2/11 | Viết báo cáo và hình | `reports/` | ✔ bản nháp |
| 14 | 3/11 | Dự phòng, sửa cuối, nộp | bản nộp | |

## 8. Học kèm (tự học khi đến bước đó)
Ngày 2: tolerance factor, octahedral factor. Ngày 4: accuracy, confusion matrix. Ngày 6: overfitting, cross-validation. Ngày 9: data leakage và vì sao chia theo nhóm. Ngày 11: trung bình, độ lệch chuẩn.
