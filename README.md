# Password Manager - Nhóm 7

> Dự án môn **An Toàn Thông Tin** — Xây dựng hệ thống quản lý mật khẩu cá nhân bằng Python

---

## Thành viên nhóm

| Thành viên | Vai trò | Nhiệm vụ |
| Họ và Tên:
| Họ và Tên:
| Họ và Tên:
| Bao | Kiến trúc & Bảo mật | Database, AES-256, logic mã hóa |
| Vinh | Giao diện & Logic | UI/UX, Password Generator |
| Quoc Bao | Báo cáo & Slide | Canva, Word report, Demo |

---

## 🗂️ Cấu trúc dự án

```
password-manager/
│
├── src/
│   ├── core/               # [BAO] Kiến trúc & Bảo mật
│   │   ├── __init__.py
│   │   ├── crypto.py       # Mã hóa AES-256, hash master password
│   │   ├── database.py     # Quản lý lưu trữ dữ liệu (SQLite)
│   │   └── vault.py        # Logic chính: thêm/sửa/xóa/tìm mật khẩu
│   │
│   ├── ui/                 # [VINH] Giao diện & Logic
│   │   ├── __init__.py
│   │   ├── app.py          # App chính (Tkinter)
│   │   ├── login_screen.py # Màn hình đăng nhập Master Password
│   │   ├── main_screen.py  # Màn hình chính (danh sách mật khẩu)
│   │   └── add_edit_screen.py # Form thêm/sửa mật khẩu
│   │
│   └── utils/              # [VINH] Tiện ích
│       ├── __init__.py
│       └── generator.py    # Password Generator tự động
│
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_crypto.py
│   └── test_vault.py
│
├── docs/                   # [QUOC BAO] Tài liệu
│   ├── bao_cao.md          # Nội dung báo cáo
│   └── huong_dan_su_dung.md
│
├── assets/                 # Ảnh, icon cho slide
│
├── main.py                 # Điểm khởi chạy ứng dụng
├── requirements.txt        # Thư viện cần cài
├── .gitignore
└── README.md
```

---

## ⚙️ Cài đặt & Chạy

```bash
# 1. Clone về máy
git clone https://github.com/<your-username>/password-manager.git
cd password-manager

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy ứng dụng
python main.py
```

---

## 🔑 Tính năng dự kiến

- [x] Cấu trúc dự án
- [ ] Mã hóa Master Password (bcrypt/PBKDF2)
- [x] Mã hóa dữ liệu AES-256
- [ ] Lưu trữ SQLite
- [x] Giao diện Tkinter
- [ ] Password Generator
- [ ] Tìm kiếm & phân loại mật khẩu
- [ ] Xuất/Nhập dữ liệu

---

## 🛠️ Công nghệ sử dụng

- **Python 3.10+**
- **cryptography** — AES-256, PBKDF2
- **tkinter** — Giao diện
- **SQLite3** — Lưu trữ (có sẵn trong Python)
- **bcrypt** — Hash Master Password
