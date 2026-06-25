"""
[VINH] Giao diện & Logic
Màn hình đăng nhập — Nhập Master Password.

TODO: Xây dựng UI tại đây
"""

import tkinter as tk
from tkinter import messagebox
from src.core.vault import Vault


class LoginScreen(tk.Frame):
    """Màn hình đăng nhập / thiết lập Master Password."""

    def __init__(self, parent, vault: Vault, on_success):
        super().__init__(parent, bg="#1e1e2e")
        self.vault = vault
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        # TODO [VINH]: Xây dựng giao diện đăng nhập ở đây
        tk.Label(self, text="[VINH] Login Screen - chưa triển khai",
                 bg="#1e1e2e", fg="white").pack(pady=50)
