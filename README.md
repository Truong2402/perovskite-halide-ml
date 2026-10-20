# Quy tắc hình học hay học máy? Dự đoán khả năng hình thành perovskite halide

Đề tài môn giới thiệu ngành khoa học vật liệu HCMUS. Nhóm so sánh các quy tắc hình học
(hệ số dung sai Goldschmidt *t*, hệ số bát diện *μ*, hệ số *τ* của Bartel và cộng sự)
với mô hình học máy đơn giản. Câu hỏi chính: kết quả có còn đúng khi mô hình phải
dự đoán một nhóm hoá học chưa từng thấy hay không.

## Kết quả chính

Chỉ số là balanced accuracy trên 207 halide ABX₃, trung bình 10 seed.

| Mô hình | Chia ngẫu nhiên | Giấu cation B | Giấu halide X |
|---|---|---|---|
| Quy tắc t | 0.650 | 0.650 | 0.650 |
| Quy tắc t + μ | 0.879 | 0.862 | 0.855 |
| τ (Bartel) | 0.918 | 0.918 | 0.918 |
| Hồi quy logistic | 0.797 | 0.779 | 0.694 |
| Cây quyết định | 0.932 | 0.903 | 0.832 |
| Random forest | 0.923 | 0.914 | 0.802 |

- Khi chia dữ liệu ngẫu nhiên, học máy và τ cho kết quả gần như nhau.
- Khi gặp halide chưa thấy, học máy giảm rõ. Gần như toàn bộ mức giảm đến từ fluoride:
  random forest chỉ đúng 63%, trong khi τ đúng 92%.

Chi tiết và các giới hạn của kết quả nằm trong [docs/experiment_log.md](docs/experiment_log.md).

## Chạy lại từ đầu

Cần cài [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python src/download_data.py
uv run pytest
uv run python src/run_experiments.py
uv run python src/plots.py
```

## Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| `src/` | Đọc dữ liệu, các quy tắc t/μ/τ, chạy thí nghiệm, vẽ hình |
| `tests/` | Kiểm tra code tái tạo đúng t, τ và dự đoán của Bartel |
| `experiments/exp001/` | Kết quả thô, bảng tổng hợp, cấu hình lần chạy |
| `reports/figures/` | Hình dùng cho slide, vẽ bằng matplotlib |
| `docs/` | Kế hoạch nghiên cứu, data card, nhật ký thí nghiệm |

## Dữ liệu và trích dẫn

Dữ liệu **không** được lưu trong kho này. `src/download_data.py` tải dữ liệu từ
[CJBartel/perovskite-stability](https://github.com/CJBartel/perovskite-stability) (giấy phép MIT).

> Bartel C. J. et al., *New tolerance factor to predict the stability of perovskite oxides and halides*,
> Science Advances 5, eaav0693 (2019). doi:10.1126/sciadv.aav0693

## Giấy phép

Code trong kho này dùng giấy phép [MIT](LICENSE). Dữ liệu thuộc về tác giả gốc, xem phần trên.
