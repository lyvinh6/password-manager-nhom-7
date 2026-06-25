"""
[VINH] Giao diện & Logic
Màn hình chính — Hiển thị danh sách mật khẩu, tìm kiếm, thêm/sửa/xóa.

TODO: Xây dựng UI tại đây
"""

import tkinter as tk
from src.core.vault import Vault


class MainScreen(tk.Frame):
    """Màn hình chính của ứng dụng."""

    def __init__(self, parent, vault: Vault, on_logout):
        super().__init__(parent, bg="#1e1e2e")
        self.vault = vault
        self.on_logout = on_logout
        self._build_ui()

    def _build_ui(self):
        # TODO [VINH]: Xây dựng layout chính ở đây
        # Gợi ý layout:
        # - Sidebar trái: danh mục (Email, Banking, Social, ...)
        # - Panel phải: danh sách mật khẩu + search bar
        # - Toolbar: nút Thêm, Sửa, Xóa, Copy, Lock
        tk.Label(self, text="[VINH] Main Screen - chưa triển khai",
                 bg="#1e1e2e", fg="white").pack(pady=50)

    def refresh(self):
        """Tải lại danh sách mật khẩu từ vault."""
        # TODO: Gọi self.vault.get_all_entries() và cập nhật UI
        pass
