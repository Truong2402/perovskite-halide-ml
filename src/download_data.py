"""Tải dữ liệu gốc của Bartel et al. (2019) vào data/raw/ — chỉ chạy một lần.

Nguồn: https://github.com/CJBartel/perovskite-stability (giấy phép MIT)
Bài báo: Bartel et al., Science Advances 5, eaav0693 (2019), DOI 10.1126/sciadv.aav0693
Script KHÔNG ghi đè file đã có, để dữ liệu gốc luôn bất biến.
"""

import hashlib
import stat
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/CJBartel/perovskite-stability/master/"
FILES = {"TableS1.csv": "TableS1.csv", "LICENSE": "LICENSE_Bartel.txt"}
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def sha256(path: Path) -> str:
    """Trả về mã băm SHA256 để kiểm tra file không bị thay đổi."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for remote, local in FILES.items():
        dest = RAW / local
        if dest.exists():
            print(f"Đã có, bỏ qua: {dest.name}  sha256={sha256(dest)}")
            continue
        urllib.request.urlretrieve(BASE + remote, dest)
        dest.chmod(stat.S_IREAD)  # chỉ đọc
        print(f"Đã tải: {dest.name}  {dest.stat().st_size} bytes  sha256={sha256(dest)}")


if __name__ == "__main__":
    main()
