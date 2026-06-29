import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="vault.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Bảng Master Config (Lưu hash mật khẩu)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS master_config (hash BLOB, salt BLOB)")
        # Bảng Passwords
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, username TEXT, password TEXT, 
                category TEXT, notes TEXT, created_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_master(self, hashed_pw, salt):
        self.cursor.execute("INSERT INTO master_config VALUES (?, ?)", (hashed_pw, salt))
        self.conn.commit()