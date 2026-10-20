# Tổng quan tài liệu v1 — Dự đoán khả năng hình thành / ổn định perovskite halide
Ngày tra cứu: 2026-10-20 · Nguồn tra cứu: arXiv.

## A. Đã kiểm chứng (đã đọc nội dung bài trên arXiv)

### Bartel et al., "New Tolerance Factor to Predict the Stability of Perovskite Oxides and Halides" — arXiv:1801.07700
- 576 hợp chất ABX3 thực nghiệm (X = O, F, Cl, Br, I), nhãn perovskite / không perovskite.
- Dùng SISSO tìm hệ số τ mới (1 chiều, diễn giải được): đúng 92%; kiểm tra ngoài tập 1.034 perovskite đơn và kép: 91%.
- Chỉ ra Goldschmidt t kém với halide: độ chính xác khoảng 51% (chloride), 56% (bromide), 33% (iodide).
- Có phân tích t, μ và cặp (t, μ); dùng bán kính sửa đổi thì độ chính xác giảm khoảng 5% → **kết quả nhạy với bộ bán kính ion**.
- → **Trùng gần như toàn bộ đề tài gốc** (so sánh t, μ với mô hình dữ liệu).

### "Stability Engineering of Halide Perovskite via Machine Learning" — arXiv:1803.06042
- Dữ liệu: năng lượng phân huỷ ΔH_d (DFT) của 354 perovskite halide.
- So sánh t và (μ + t): độ chính xác dự đoán formability (relative stability) 68% (80%) và 85% (90%).
- Huấn luyện ML, áp dụng sàng lọc 14.190 perovskite kép halide.
- → **Trùng với hướng "so sánh t/μ với ML" trên halide.**

### Các bài liên quan khác (mới đọc tóm tắt)
- arXiv:2510.06166 (Purdue, 2025): khả năng tổng hợp (synthesizability) perovskite halide/chalcogenide; kết hợp DFT, dữ liệu tài liệu và PU learning.
- arXiv:2312.11335 (2023): bộ dữ liệu ABX3 vô cơ cho ML.
- arXiv:2605.21650, 2605.22887 (2026): sàng lọc perovskite kép không chì có thể diễn giải, kiểm chứng bằng DFT.
- arXiv:2504.04002 (2025): ML cho độ ổn định nhiệt theo thành phần (perovskite lai).

## B. Biết từ kiến thức nền — CHƯA kiểm chứng trong phiên này (cần tra DOI trước khi trích dẫn)
- Li et al. (khoảng 2004–2008): bản đồ t–μ cho formability của halide ABX3.
- Travis et al., Chem. Sci. 2016: bán kính ion sửa đổi cho halide (bài 1803.06042 trích dẫn "a revised system", Chem. Sci. 7, 4548).
- Filip & Giustino, PNAS 2018: tiêu chí hình học cho perovskite.
- Pilania et al. (khoảng 2016): ML phân loại formability của ABX3.

## C. Kết luận về mức trùng lặp
Đề tài gốc ("so sánh t và μ với ML đơn giản cho perovskite halide") **đã được làm nhiều lần từ 2016–2019**, kể cả cùng bộ dữ liệu công khai. Nếu làm y nguyên thì chỉ là bài tập tái lập (replication), không có tính mới.

Khoảng trống còn lại phù hợp sức sinh viên năm 1:
1. Hầu hết bài báo cáo độ chính xác với chia dữ liệu ngẫu nhiên → chưa rõ t, μ, τ, ML **có ngoại suy được sang hoá học chưa thấy** (cation B mới, halide khác) hay không.
2. Kết quả nhạy với bộ bán kính ion (Bartel: khoảng 5%) nhưng ít được lượng hoá có hệ thống.
3. Dữ liệu ít (vài trăm mẫu) → mô hình phức tạp dễ overfit; cần so sánh công bằng và độ bất định.
