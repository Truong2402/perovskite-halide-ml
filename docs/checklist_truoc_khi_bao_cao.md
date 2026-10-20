# Checklist trước khi báo cáo / nộp

- [ ] Mọi con số trong báo cáo truy được về experiments/ hoặc nguồn có DOI
- [ ] Có baseline và mô hình hơn baseline qua ≥ 5 seed (mean ± std)
- [ ] Chia dữ liệu theo nhóm công thức; chuẩn hoá/chọn đặc trưng chỉ fit trên train
- [ ] Tập test dùng đúng 1 lần
- [ ] Có biểu đồ predicted vs. actual, phân bố sai số, và ví dụ dự đoán sai nhiều nhất
- [ ] Đơn vị đầy đủ; dự đoán nằm trong miền hợp lý vật lý
- [ ] Nêu giới hạn (miền dữ liệu, thiên lệch DFT, cỡ mẫu)
- [ ] data_card.md điền đủ; license cho phép dùng
- [ ] Chạy lại từ đầu bằng `uv sync` + script cho ra cùng kết quả
- [ ] Ghi rõ phần có AI hỗ trợ; tôi giải thích được từng đoạn code và phương pháp
- [ ] Không còn khoá API trong file/lịch sử git
