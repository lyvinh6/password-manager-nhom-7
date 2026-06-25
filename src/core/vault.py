"""
[BAO] Kiến trúc & Bảo mật
Vault - Lớp trung gian kết nối crypto và database.
Đây là nơi xử lý logic chính của ứng dụng.
"""

import os
from src.core import crypto, database


class Vault:
    """
    Quản lý toàn bộ vòng đời của password vault.
    Cần được khởi tạo và unlock bằng Master Password trước khi dùng.
    """

    def __init__(self):
        self._key: bytes | None = None  # Khóa AES, chỉ có khi đã unlock
        database.init_db()

    # ─── Thiết lập & Đăng nhập ──────────────────────────────────────────────

    def is_setup(self) -> bool:
        """Kiểm tra đã có Master Password chưa."""
        return database.get_master() is not None

    def setup(self, master_password: str):
        """
        Lần đầu: tạo Master Password, sinh salt và lưu vào DB.
        Gọi khi người dùng chưa có vault.
        """
        salt = os.urandom(32)
        hashed = crypto.hash_master_password(master_password)
        database.save_master(hashed, salt)
        self._key = crypto.derive_key(master_password, salt)

    def unlock(self, master_password: str) -> bool:
        """
        Xác thực Master Password và nạp khóa AES vào bộ nhớ.
        Trả về True nếu thành công.
        """
        master = database.get_master()
        if not master:
            return False
        if not crypto.verify_master_password(master_password, master["hash"]):
            return False
        self._key = crypto.derive_key(master_password, master["salt"])
        return True

    def lock(self):
        """Khóa vault — xóa khóa AES khỏi bộ nhớ."""
        self._key = None

    @property
    def is_unlocked(self) -> bool:
        return self._key is not None

    def _require_unlock(self):
        if not self.is_unlocked:
            raise PermissionError("Vault chưa được mở khóa. Vui lòng đăng nhập.")

    # ─── CRUD ───────────────────────────────────────────────────────────────

    def add_entry(self, title: str, username: str, password: str,
                   url: str = "", category: str = "Khác", notes: str = "") -> int:
        """Mã hóa mật khẩu và lưu vào DB."""
        self._require_unlock()
        encrypted = crypto.encrypt(password, self._key)
        return database.add_password(title, username, encrypted, url, category, notes)

    def get_all_entries(self) -> list[dict]:
        """Lấy danh sách tất cả entry (mật khẩu vẫn còn mã hóa)."""
        self._require_unlock()
        return database.get_all_passwords()

    def get_entry(self, entry_id: int) -> dict | None:
        """Lấy một entry và giải mã mật khẩu."""
        self._require_unlock()
        entry = database.get_password_by_id(entry_id)
        if entry:
            entry["password"] = crypto.decrypt(entry["password"], self._key)
        return entry

    def update_entry(self, entry_id: int, title: str, username: str, password: str,
                      url: str = "", category: str = "Khác", notes: str = ""):
        """Cập nhật entry — mã hóa lại mật khẩu mới."""
        self._require_unlock()
        encrypted = crypto.encrypt(password, self._key)
        database.update_password(entry_id, title, username, encrypted, url, category, notes)

    def delete_entry(self, entry_id: int):
        """Xóa entry."""
        self._require_unlock()
        database.delete_password(entry_id)

    def search(self, keyword: str) -> list[dict]:
        """Tìm kiếm entry theo từ khóa."""
        self._require_unlock()
        return database.search_passwords(keyword)
