"""
[VINH] Giao diện & Logic
Form thêm / sửa mật khẩu.

TODO: Xây dựng UI tại đây
"""

import tkinter as tk
from tkinter import ttk
from src.core.vault import Vault
from src.utils.generator import generate_password, check_strength


class AddEditScreen(tk.Toplevel):
    """
    Cửa sổ popup để thêm hoặc chỉnh sửa một mật khẩu.
    Nếu entry_id=None → chế độ thêm mới.
    """

    def __init__(self, parent, vault: Vault, on_save, entry_id: int | None = None):
        super().__init__(parent)
        self.vault = vault
        self.on_save = on_save
        self.entry_id = entry_id
        self.title("Thêm mật khẩu" if entry_id is None else "Sửa mật khẩu")
        self.geometry("500x450")
        self._build_ui()

        if entry_id is not None:
            self._load_entry(entry_id)

    def _build_ui(self):
        # TODO [VINH]: Xây dựng form nhập liệu ở đây
        # Các trường: title, username, password (+ nút Generate), url, category, notes
        # Nút Save và Cancel
        tk.Label(self, text="[VINH] Add/Edit Form - chưa triển khai").pack(pady=50)

    def _load_entry(self, entry_id: int):
        """Tải dữ liệu entry để sửa."""
        entry = self.vault.get_entry(entry_id)
        if entry:
            pass  # TODO: Điền vào các field

    def _on_generate(self):
        """Tạo mật khẩu ngẫu nhiên và điền vào field."""
        pwd = generate_password(length=16)
        # TODO: Điền pwd vào password field

    def _on_save(self):
        """Lưu entry vào vault."""
        # TODO: Lấy dữ liệu từ form và gọi vault.add_entry() hoặc vault.update_entry()
        pass
