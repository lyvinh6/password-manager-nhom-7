# 🔐 Password Manager - Nhóm 7

> Dự án môn **An Toàn Thông Tin** — Xây dựng hệ thống quản lý mật khẩu cá nhân bằng Python

---

## 👥 Thành viên nhóm

| Thành viên | Vai trò | Nhiệm vụ |
|---|---|---|
| Bao | Kiến trúc & Bảo mật | Database, AES-256, logic mã hóa |
| Vinh | Giao diện & Logic | UI/UX, Password Generator |
| Quoc Bao | Báo cáo & Slide | Canva, Word report, Demo |

---
Demo giao diện
Màn hình đăng nhập / đăng ký
<img width="1023" height="887" alt="image" src="https://github.com/user-attachments/assets/aaf261d2-2972-45a4-a164-bb62d2f8e02d" />
Màn hình Dashboard — quản lý mật khẩu
<img width="1022" height="888" alt="image" src="https://github.com/user-attachments/assets/50d469bf-a164-436b-af68-04911102398c" />

## 🗂️ Cấu trúc dự án

```
password-manager-nhom-7/
│
├── main.py                 # ⭐ Điểm khởi chạy chính của ứng dụng (CustomTkinter UI)
├── crypto.py                # Hash/verify Master Password bằng bcrypt (module độc lập)
├── database.py               # [Legacy] Bản SQLite cũ, không còn được main.py sử dụng
├── vault.py                  # [Legacy] Bản nháp lớp Vault SQLite, chưa hoàn thiện
│
├── core/                    # ⭐ Module lõi đang được main.py sử dụng thực tế
│   ├── __init__.py
│   ├── crypto_utils.py       # CryptoManager: sinh salt, dẫn xuất khóa PBKDF2, mã hóa AES-256-GCM
│   └── db_manager.py         # VaultDB: lưu/đọc két sắt theo Username trên SQL Server (pyodbc)
│
├── src/                      # [Scaffold] Kiến trúc dự kiến ban đầu theo mô hình SQLite phân lớp
│   ├── core/
│   │   ├── crypto.py          # Bản AES-256-GCM + bcrypt dùng SQLite (song song với core/)
│   │   ├── database.py        # CRUD SQLite (tương tự core/db_manager.py nhưng dùng sqlite3)
│   │   └── vault.py           # Lớp Vault trung gian (setup/unlock/lock/CRUD)
│   ├── ui/                    # Khung giao diện Tkinter thuần — hầu hết còn ở dạng TODO
│   │   ├── app.py
│   │   ├── login_screen.py
│   │   ├── main_screen.py
│   │   └── add_edit_screen.py
│   └── utils/
│       └── generator.py       # Sinh mật khẩu ngẫu nhiên (secrets) + đánh giá độ mạnh
│
├── tests/                    # Unit test cho bộ core của src/ (pytest)
│   ├── test_crypto.py
│   └── test_vault.py
│
├── docs/
│   └── bao_cao_outline.md     # Đề cương báo cáo của nhóm
│
├── assets/                   # Ảnh chụp giao diện demo, dùng cho README/slide
│   ├── screenshot_login.png
│   └── screenshot_dashboard.png
│
├── SETUP_GITHUB.sh           # Script tiện ích đẩy code lên GitHub lần đầu
├── requirements.txt
└── README.md
```

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
- [x] Password Generator
- [ ] Tìm kiếm & phân loại mật khẩu
- [x] Xuất/Nhập dữ liệu

---

## 🛠️ Công nghệ sử dụng

- **Python 3.10+**
- **cryptography** — AES-256, PBKDF2
- **tkinter** — Giao diện
- **SQLite3** — Lưu trữ (có sẵn trong Python)
- **bcrypt** — Hash Master Password
