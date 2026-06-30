🔐 Password Manager Advance - Nhóm 7


Đồ án môn An Toàn Thông Tin — Xây dựng hệ thống quản lý mật khẩu cá nhân bằng Python, sử dụng mã hóa AES-256-GCM, dẫn xuất khóa PBKDF2-HMAC-SHA256 và lưu trữ trên SQL Server.




👥 Thành viên nhóm

Thành viênVai tròNhiệm vụBaoKiến trúc & Bảo mậtDatabase, mã hóa AES-256-GCM, dẫn xuất khóa, logic mã hóaVinhGiao diện & LogicUI/UX (CustomTkinter), kiểm tra độ phức tạp mật khẩu, Password GeneratorQuoc BaoBáo cáo & SlideCanva, Word report, Demo


🚀 Tổng quan

Ứng dụng cho phép người dùng tạo một Master Password duy nhất để mở "két sắt" mật khẩu của riêng mình. Mọi dữ liệu tài khoản (tên đăng nhập, mật khẩu, ghi chú...) được mã hóa bằng AES-256-GCM trước khi lưu lên SQL Server, theo mô hình Zero-Knowledge: máy chủ chỉ lưu dữ liệu đã mã hóa, không bao giờ biết hay lưu trữ Master Password gốc dưới bất kỳ hình thức nào.


🗂️ Cấu trúc dự án

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
├── SETUP_GITHUB.sh           # Script tiện ích đẩy code lên GitHub lần đầu
├── requirements.txt
└── README.md


⚠️ Lưu ý về cấu trúc: Dự án hiện có 2 nhánh hiện thực song song:


Bản đang chạy thật (main.py ở thư mục gốc + core/crypto_utils.py + core/db_manager.py): dùng CustomTkinter + SQL Server (qua pyodbc). Đây là bản chính thức để build/nộp/demo.
Bản scaffold ban đầu (src/): dùng Tkinter thuần + SQLite, được dựng sẵn cấu trúc nhưng phần UI (src/ui/*) phần lớn còn là TODO, chưa hoàn thiện giao diện.


database.py và vault.py ở thư mục gốc là bản nháp cũ, không còn được main.py gọi tới — nhóm nên dọn dẹp hoặc gộp lại trước khi nộp bài để tránh gây nhầm lẫn cho người chấm.




⚙️ Cài đặt & Chạy

1. Yêu cầu hệ thống


Python 3.10+
SQL Server LocalDB (đi kèm Visual Studio, hoặc cài riêng SQL Server Express LocalDB)
ODBC Driver 17 for SQL Server (tải tại đây)


2. Clone về máy

bashgit clone https://github.com/lyvinh6/password-manager-nhom-7.git
cd password-manager-nhom-7

3. Cài thư viện

bashpip install -r requirements.txt


⚠️ requirements.txt hiện chưa khai báo đủ các thư viện mà main.py thực sự import (customtkinter, pyodbc). Cần bổ sung — xem mục Thư viện sử dụng bên dưới để cài thủ công nếu gặp lỗi ModuleNotFoundError.



4. Khởi tạo cơ sở dữ liệu SQL Server

Tạo database MasterPasswordDB trên SQL Server LocalDB và bảng UserVaults:

sqlCREATE DATABASE MasterPasswordDB;
GO
USE MasterPasswordDB;
GO
CREATE TABLE UserVaults (
    Username    NVARCHAR(100) PRIMARY KEY,
    Salt        NVARCHAR(MAX) NOT NULL,
    Nonce       NVARCHAR(MAX) NOT NULL,
    Ciphertext  NVARCHAR(MAX) NOT NULL
);

5. Chạy ứng dụng

bashpython main.py


🔑 Tính năng


 Đăng ký / đăng nhập bằng Master Password
 Kiểm tra độ phức tạp mật khẩu (regex: hoa, thường, số, ký tự đặc biệt, ≥ 8 ký tự)
 Mã hóa dữ liệu AES-256-GCM (Authenticated Encryption)
 Dẫn xuất khóa PBKDF2-HMAC-SHA256 (600.000 vòng lặp)
 Lưu trữ trên SQL Server (qua pyodbc)
 Thêm / xem danh sách tài khoản đã lưu
 Sao chép mật khẩu an toàn vào clipboard (pyperclip)
 Đăng xuất — xóa dữ liệu nhạy cảm khỏi RAM
 Password Generator (sinh mật khẩu ngẫu nhiên bằng module secrets)
 Sửa / xóa từng tài khoản riêng lẻ (hiện chỉ hỗ trợ thêm mới + xem)
 Tìm kiếm & phân loại mật khẩu theo category
 Cơ chế khôi phục khi quên Master Password
 Hoàn thiện giao diện ở nhánh src/ui/ (đang là TODO)
 Xuất/Nhập dữ liệu



🛠️ Thư viện sử dụng

Thư việnMục đíchcryptographyPBKDF2HMAC (dẫn xuất khóa), AESGCM (mã hóa/giải mã có xác thực)bcryptHash Master Password (module crypto.py)pyodbcKết nối và truy vấn SQL Server LocalDBcustomtkinterGiao diện hiện đại dựa trên TkinterpyperclipSao chép mật khẩu vào clipboard hệ điều hành

Cài thủ công nếu requirements.txt thiếu:

bashpip install cryptography bcrypt pyodbc customtkinter pyperclip


🧪 Kiểm thử

Bộ test hiện có (tests/test_crypto.py, tests/test_vault.py) kiểm thử nhánh src/core/ (bản SQLite). Chạy bằng:

bashpython -m pytest tests/


Lưu ý: bộ test này chưa bao phủ nhánh core/ (bản SQL Server đang chạy thật). Nhóm nên bổ sung test riêng cho core/crypto_utils.py và core/db_manager.py trước khi nộp bài để đảm bảo độ tin cậy của báo cáo kiểm thử.




🔒 Mô hình bảo mật tóm tắt


Master Password → PBKDF2-HMAC-SHA256 (600.000 vòng, salt 16 byte ngẫu nhiên) → khóa AES-256.
Dữ liệu két sắt (JSON) → AES-256-GCM (nonce 12 byte ngẫu nhiên) → ciphertext + authentication tag.
Salt, Nonce, Ciphertext được mã hóa Base64 và lưu trên SQL Server theo từng Username.
Đăng nhập = dẫn xuất lại khóa từ Master Password vừa nhập + salt đã lưu, rồi thử giải mã. Giải mã thành công (tag hợp lệ) = xác thực đúng; sai mật khẩu hoặc dữ liệu bị sửa → giải mã thất bại, trả None.
SQL Server không bao giờ lưu Master Password gốc dưới bất kỳ hình thức nào → kiến trúc Zero-Knowledge.



⚠️ Hạn chế đã biết


Toàn bộ độ an toàn phụ thuộc vào việc người dùng giữ bí mật Master Password; không có cơ chế khôi phục nếu quên.
Mỗi lần thêm/sửa, toàn bộ két sắt được mã hóa và ghi đè lại (không mã hóa từng bản ghi riêng lẻ) — kém hiệu quả khi số lượng tài khoản lưu trữ rất lớn.
Tồn tại 2 nhánh code song song (core/ và src/core/) gây trùng lặp logic, cần hợp nhất ở phiên bản sau.
requirements.txt chưa liệt kê đầy đủ dependency thực tế.



📄 Giấy phép

Dự án phục vụ mục đích học tập trong khuôn khổ môn An Toàn Thông Tin, không sử dụng cho mục đích thương mại.
