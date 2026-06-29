"""
[VINH] Giao diện & Logic
App chính — Khởi động ứng dụng Tkinter.
"""

import tkinter as tk
from src.core.vault import Vault


class App:
    """Lớp chính quản lý cửa sổ và điều hướng màn hình."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Password Manager - Nhóm 7")
        self.root.geometry("900x600")
        self.root.minsize(700, 450)

        self.vault = Vault()
        self._current_frame = None

    def run(self):
        """Khởi chạy ứng dụng."""
        self._show_login()
        self.root.mainloop()

    def _clear_frame(self):
        """Xóa màn hình hiện tại."""
        if self._current_frame:
            self._current_frame.destroy()

    def _show_login(self):
        """Hiển thị màn hình đăng nhập."""
        self._clear_frame()
        # TODO [VINH]: Import và hiển thị LoginScreen
        # from src.ui.login_screen import LoginScreen
        # self._current_frame = LoginScreen(self.root, self.vault, on_success=self._show_main)
        # self._current_frame.pack(fill="both", expand=True)

        # Placeholder tạm thời
        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(fill="both", expand=True)
        tk.Label(
            frame,
            text="🔐 Password Manager",
            font=("Helvetica", 28, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=(120, 10))
        tk.Label(
            frame,
            text="[VINH] Xây dựng giao diện đăng nhập tại đây\nsrc/ui/login_screen.py",
            font=("Helvetica", 13),
            bg="#1e1e2e", fg="#6c7086"
        ).pack()
        self._current_frame = frame

    def _show_main(self):
        """Hiển thị màn hình chính sau khi đăng nhập."""
        self._clear_frame()
        # TODO [VINH]: Import và hiển thị MainScreen
        # from src.ui.main_screen import MainScreen
        # self._current_frame = MainScreen(self.root, self.vault, on_logout=self._show_login)
        # self._current_frame.pack(fill="both", expand=True)
        pass
