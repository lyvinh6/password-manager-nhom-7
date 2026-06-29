# File: main.py
import customtkinter as ctk
import tkinter.messagebox as messagebox
import re
import pyperclip  # Thư viện để tự động Copy vào bộ nhớ đệm máy tính
from core.db_manager import VaultDB

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager Advance - Nhóm 7")
        self.geometry("820x680") # Kích thước chuẩn tối ưu cho giao diện

        self.current_username = None
        self.current_master_pwd = None
        self.vault_data = None

        # ==========================================
        # 1. KHUNG ĐĂNG NHẬP / ĐĂNG KÝ
        # ==========================================
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=80, padx=50, fill="both", expand=True)

        self.lbl_title = ctk.CTkLabel(self.login_frame, text="🔒 SQL PASSWORD MANAGER v2.0", font=("Arial", 24, "bold"))
        self.lbl_title.pack(pady=(40, 20))

        self.entry_username = ctk.CTkEntry(self.login_frame, placeholder_text="Nhập Username...", width=280)
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.login_frame, placeholder_text="Nhập Master Password...", show="*", width=280)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self.login_frame, text="Mở Khóa Vault", width=280, font=("Arial", 14, "bold"), command=self.unlock_vault)
        self.btn_login.pack(pady=10)
        
        self.btn_create = ctk.CTkButton(self.login_frame, text="Đăng Ký Tài Khoản Mới", width=280, fg_color="green", hover_color="darkgreen", command=self.create_vault)
        self.btn_create.pack(pady=10)

        self.dashboard_frame = ctk.CTkFrame(self)

    def check_password_complexity(self, password):
        if len(password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự!"
        if not re.search(r"[a-z]", password):
            return False, "Mật khẩu phải chứa chữ cái viết THƯỜNG (a-z)!"
        if not re.search(r"[A-Z]", password):
            return False, "Mật khẩu phải chứa chữ cái viết HOA (A-Z)!"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\/`~;']", password):
            return False, "Mật khẩu phải chứa ký tự đặc biệt (!@#$...)!"
        return True, "Hợp lệ"

    def unlock_vault(self):
        username = self.entry_username.get().strip()
        master_pwd = self.entry_password.get().strip()
        
        if not username or not master_pwd:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ Username và Mật khẩu!")
            return

        data = VaultDB.load_vault(username, master_pwd)

        if data == "NO_DB":
            messagebox.showerror("Lỗi", "Tài khoản không tồn tại trên hệ thống SQL Server!")
        elif data is None:
            messagebox.showerror("Lỗi", "Sai Master Password! Không thể giải mã dữ liệu.")
        else:
            self.current_username = username
            self.current_master_pwd = master_pwd
            self.vault_data = data
            self.show_dashboard() 

    def create_vault(self):
        username = self.entry_username.get().strip()
        master_pwd = self.entry_password.get().strip()
        
        if not username or not master_pwd:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin đăng ký!")
            return
            
        is_valid, msg = self.check_password_complexity(master_pwd)
        if not is_valid:
            messagebox.showerror("Mật khẩu yếu", f"Đăng ký thất bại:\n{msg}")
            return
            
        initial_data = {"my_accounts": []}
        
        try:
            VaultDB.save_vault(username, master_pwd, initial_data)
            messagebox.showinfo("Thành công", f"Đã đăng ký tài khoản '{username}' an toàn trên SQL Server!")
        except Exception as e:
            messagebox.showerror("Lỗi SQL", f"Không thể kết nối SQL Server:\n{e}")

    # ==========================================
    # 2. HÀM XỬ LÝ ĐĂNG XUẤT (BẢO MẬT)
    # ==========================================
    def logout(self):
        """Xóa dữ liệu nhạy cảm khỏi RAM và quay về màn hình Login"""
        self.current_username = None
        self.current_master_pwd = None
        self.vault_data = None
        
        # Xóa các ký tự đã nhập ở ô đăng nhập để an toàn
        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        
        # Chuyển đổi Frame giao diện
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(pady=80, padx=50, fill="both", expand=True)
        messagebox.showinfo("Két sắt đã đóng", "Đã đăng xuất và khóa két sắt an toàn!")

    # ==========================================
    # 3. GIAO DIỆN DASHBOARD CHI TIẾT
    # ==========================================
    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Xóa sạch các widget cũ trong Dashboard phòng trường hợp đăng nhập lại bị trùng lặp
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # ------------------------------------------
        # THANH TIÊU ĐỀ + NÚT THOÁT ĐĂNG XUẤT
        # ------------------------------------------
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5, padx=5)

        lbl_dash_title = ctk.CTkLabel(
            header_frame, 
            text=f"QUẢN LÍ MẬT KHẨU - Người dùng: {self.current_username}", 
            font=("Arial", 20, "bold")
        )
        lbl_dash_title.pack(side="left", padx=10)

        # Nút Đăng xuất màu đỏ đậm sang xịn mịn
        btn_logout = ctk.CTkButton(
            header_frame, 
            text="🔒 Đăng Xuất", 
            fg_color="#A30000", 
            hover_color="#7A0000", 
            width=110, 
            font=("Arial", 12, "bold"), 
            command=self.logout
        )
        btn_logout.pack(side="right", padx=10)

        # Vùng cuộn xem danh sách tài khoản
        self.scroll_frame = ctk.CTkScrollableFrame(self.dashboard_frame, width=750, height=340)
        self.scroll_frame.pack(pady=10, fill="both", expand=True)

        # ------------------------------------------
        # FORM THÊM MỚI
        # ------------------------------------------
        form_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="gray15", border_width=1, border_color="gray25")
        form_frame.pack(pady=10, fill="x", padx=5)

        lbl_form_title = ctk.CTkLabel(form_frame, text=" THÊM TÀI KHOẢN ĐA THÔNG TIN", font=("Arial", 12, "bold"), text_color="#1f538d")
        lbl_form_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(8, 2), sticky="w")

        # Dòng 1: Tên Ứng dụng, Tài khoản, Mật khẩu
        self.entry_new_site = ctk.CTkEntry(form_frame, placeholder_text="Tên ứng dụng (Ví dụ: Facebook...)", width=240)
        self.entry_new_site.grid(row=1, column=0, padx=10, pady=5)

        self.entry_new_user = ctk.CTkEntry(form_frame, placeholder_text="Tên đăng nhập / Email", width=240)
        self.entry_new_user.grid(row=1, column=1, padx=10, pady=5)

        self.entry_new_pwd = ctk.CTkEntry(form_frame, placeholder_text="Mật khẩu bảo mật", show="*", width=240)
        self.entry_new_pwd.grid(row=1, column=2, padx=10, pady=5)

        # Dòng 2: Đường dẫn URL, Ghi chú thêm, Nút Lưu
        self.entry_new_url = ctk.CTkEntry(form_frame, placeholder_text="Đường dẫn trang web (https://...)", width=240)
        self.entry_new_url.grid(row=2, column=0, padx=10, pady=(5, 12))

        self.entry_new_notes = ctk.CTkEntry(form_frame, placeholder_text="Ghi chú thêm...", width=240)
        self.entry_new_notes.grid(row=2, column=1, padx=10, pady=(5, 12))

        btn_add = ctk.CTkButton(form_frame, text="Lưu Vào Két Sắt", width=240, fg_color="green", hover_color="darkgreen", font=("Arial", 13, "bold"), command=self.add_new_credential)
        btn_add.grid(row=2, column=2, padx=10, pady=(5, 12))

        self.load_passwords_to_ui()

    def load_passwords_to_ui(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        accounts = self.vault_data.get("my_accounts", [])
        
        if not accounts:
            lbl_empty = ctk.CTkLabel(self.scroll_frame, text="Két sắt đang trống. Hãy điền form bên dưới để lưu mật khẩu đầu tiên!", font=("Arial", 14, "italic"), text_color="gray")
            lbl_empty.pack(pady=40)
            return

        for acc in accounts:
            card_frame = ctk.CTkFrame(self.scroll_frame, fg_color="gray18", border_width=1, border_color="gray30")
            card_frame.pack(fill="x", pady=6, padx=5)
            
            info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            info_frame.pack(side="left", padx=15, pady=10, fill="both", expand=True)

            lbl_site = ctk.CTkLabel(info_frame, text=f"🌐 {acc['site'].upper()}", font=("Arial", 15, "bold"), text_color="#1f538d")
            lbl_site.pack(anchor="w")

            lbl_user = ctk.CTkLabel(info_frame, text=f"👤 Tài khoản: {acc['user']}", font=("Arial", 13))
            lbl_user.pack(anchor="w", pady=2)

            url_val = acc.get('url', 'Không có Link')
            notes_val = acc.get('notes', 'Không có ghi chú')

            lbl_url = ctk.CTkLabel(info_frame, text=f"🔗 Link: {url_val}", font=("Arial", 12, "italic"), text_color="gray60")
            lbl_url.pack(anchor="w")

            lbl_notes = ctk.CTkLabel(info_frame, text=f" Ghi chú: {notes_val}", font=("Arial", 12), text_color="gray70")
            lbl_notes.pack(anchor="w", pady=2)

            actions_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            actions_frame.pack(side="right", padx=15, pady=10)

            btn_show = ctk.CTkButton(actions_frame, text=f"Mật khẩu: {acc['password']}", fg_color="gray28", hover_color="gray35", width=160)
            btn_show.pack(side="top", pady=2)

            btn_copy = ctk.CTkButton(actions_frame, text=" Copy Mật Khẩu", fg_color="#1f538d", hover_color="#14375e", width=160,
                                     command=lambda p=acc['password']: self.copy_to_clipboard(p))
            btn_copy.pack(side="top", pady=2)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        messagebox.showinfo("Clipboard", "Đã sao chép mật khẩu vào bộ nhớ tạm!")

    def add_new_credential(self):
        site = self.entry_new_site.get().strip()
        user = self.entry_new_user.get().strip()
        pwd = self.entry_new_pwd.get().strip()
        url = self.entry_new_url.get().strip()
        notes = self.entry_new_notes.get().strip()

        if not site or not user or not pwd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền tối thiểu Tên ứng dụng, Tài khoản và Mật khẩu!")
            return

        is_valid, msg = self.check_password_complexity(pwd)
        if not is_valid:
            messagebox.showerror("Mật khẩu yếu", f"Không thể thêm tài khoản:\n{msg}")
            return

        if not url: url = "Không có Link"
        if not notes: notes = "Không có ghi chú"

        if "my_accounts" not in self.vault_data:
            self.vault_data["my_accounts"] = []
            
        self.vault_data["my_accounts"].append({
            "site": site,
            "user": user,
            "password": pwd,
            "url": url,
            "notes": notes
        })

        try:
            VaultDB.save_vault(self.current_username, self.current_master_pwd, self.vault_data)
            messagebox.showinfo("Thành công", f"Đã mã hóa và lưu trữ thành công tài khoản '{site}'!")
            
            self.entry_new_site.delete(0, 'end')
            self.entry_new_user.delete(0, 'end')
            self.entry_new_pwd.delete(0, 'end')
            self.entry_new_url.delete(0, 'end')
            self.entry_new_notes.delete(0, 'end')
            
            self.load_passwords_to_ui()
            
        except Exception as e:
            messagebox.showerror("Lỗi lưu dữ liệu", f"Không thể ghi dữ liệu lên SQL Server:\n{e}")

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()