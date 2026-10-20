# Data card

| Mục | Nội dung |
|---|---|
| Tên bộ dữ liệu | TableS1 — 576 chất rắn ABX3 có phân loại thực nghiệm |
| Nguồn | https://github.com/CJBartel/perovskite-stability (tải bằng `src/download_data.py`) |
| Bài báo gốc | Bartel C. J. et al., "New tolerance factor to predict the stability of perovskite oxides and halides", Science Advances 5, eaav0693 (2019). DOI 10.1126/sciadv.aav0693 · arXiv:1801.07700 |
| Ngày tải | 2026-10-20 |
| License | MIT (bản sao: `data/raw/LICENSE_Bartel.txt`) — được dùng, cần trích dẫn |
| Tập dùng trong đề tài | 207 halide (F 66, Cl 71, Br 27, I 43); 81 perovskite / 126 không |
| Biến mục tiêu | `exp_label`: +1 perovskite, −1 không perovskite (theo thực nghiệm, ở điều kiện thường) |
| Đầu vào | rA, rB, rX (Å, bán kính Shannon), nA, nB (số oxi hoá), t, tau |
| Đặc trưng tự tạo | μ = rB / rX |
| Thiên lệch đã biết | Cột bán kính bị làm tròn 2 chữ số (vd. Co²⁺ 0.745 → 0.74 Å); cột tau tính từ giá trị chưa làm tròn. τ được tìm trên chính bộ dữ liệu này (172/207 halide thuộc tập train của Bartel). Br chỉ có 27 mẫu. Fluoride chủ yếu là perovskite (51/66), các halide khác chủ yếu không. |
| SHA256 TableS1.csv | bea471ddb1ed63dcb94cc9cbc58c73f3bc1a12918e96cf24818b3aea2cbe3656 |
| Script xử lý | `src/data.py` (lọc halide, tạo y và μ), không ghi file trung gian |
