# File: core/db_manager.py
import pyodbc
import base64
from .crypto_utils import CryptoManager

# CẤU HÌNH KẾT NỐI ĐẾN SQL SERVER LOCALDB
# Lưu ý: Dấu hai gạch chéo \\ ở phần SERVER là bắt buộc để Python hiểu ký tự đặc biệt
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=MasterPasswordDB;"
    "Trusted_Connection=yes;"
)

class VaultDB:
    @staticmethod
    def save_vault(username: str, master_password: str, data: dict):
        """Mã hóa và lưu (hoặc cập nhật) dữ liệu của một User lên SQL Server"""
        salt = CryptoManager.generate_salt()
        key = CryptoManager.derive_key(master_password, salt)
        
        nonce, ciphertext = CryptoManager.encrypt_data(key, data)

        # Chuyển đổi dữ liệu bytes sang chuỗi Base64 để lưu vào SQL Server
        salt_str = base64.b64encode(salt).decode('utf-8')
        nonce_str = base64.b64encode(nonce).decode('utf-8')
        ciphertext_str = base64.b64encode(ciphertext).decode('utf-8')

        # Thực hiện kết nối Cơ sở dữ liệu
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()

        # Kiểm tra xem tài khoản (Username) này đã tồn tại trong SQL Server chưa
        cursor.execute("SELECT Username FROM UserVaults WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if row:
            # Nếu đã tồn tại -> Tiến hành cập nhật lại két sắt (UPDATE)
            cursor.execute("""
                UPDATE UserVaults 
                SET Salt = ?, Nonce = ?, Ciphertext = ? 
                WHERE Username = ?
            """, (salt_str, nonce_str, ciphertext_str, username))
        else:
            # Nếu chưa tồn tại -> Thêm mới tài khoản và két sắt (INSERT)
            cursor.execute("""
                INSERT INTO UserVaults (Username, Salt, Nonce, Ciphertext) 
                VALUES (?, ?, ?, ?)
            """, (username, salt_str, nonce_str, ciphertext_str))

        # Xác nhận lưu thay đổi và đóng kết nối
        conn.commit()
        cursor.close()
        conn.close()
            
        # Zero-Knowledge: Xóa key khỏi RAM ngay sau khi hoàn thành
        del key 

    @staticmethod
    def load_vault(username: str, master_password: str):
        """Tải dữ liệu mã hóa từ SQL Server về và thực hiện giải mã"""
        
        # Thực hiện kết nối Cơ sở dữ liệu
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()

        # Lấy Salt, Nonce và Ciphertext theo đúng Username đăng nhập
        cursor.execute("SELECT Salt, Nonce, Ciphertext FROM UserVaults WHERE Username = ?", (username,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        # Nếu không tìm thấy dòng dữ liệu nào ứng với Username này
        if not row:
            return "NO_DB" # Tài khoản không tồn tại trên hệ thống

        # Giải mã các chuỗi mã hóa Base64 ngược lại thành định dạng Bytes ban đầu
        salt = base64.b64decode(row[0])
        nonce = base64.b64decode(row[1])
        ciphertext = base64.b64decode(row[2])

        # Thử tạo khóa giải mã dựa trên Master Password mà người dùng vừa nhập vào
        key = CryptoManager.derive_key(master_password, salt)
        
        # Tiến hành giải mã cục dữ liệu Ciphertext
        decrypted_data = CryptoManager.decrypt_data(key, nonce, ciphertext)
        
        # Zero-Knowledge: Xóa key khỏi RAM
        del key
        
        return decrypted_data