"""
[BAO] Kiến trúc & Bảo mật
Module quản lý cơ sở dữ liệu SQLite.

Schema:
  - master_config: Lưu hash Master Password và salt mã hóa
  - passwords: Lưu các mật khẩu đã mã hóa
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("vault.db")


def get_connection() -> sqlite3.Connection:
    """Tạo và trả về kết nối SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Trả về dict-like rows
    return conn


def init_db():
    """Khởi tạo database và tạo bảng nếu chưa có."""
    conn = get_connection()
    cursor = conn.cursor()

    # Bảng cấu hình master (chỉ có 1 dòng)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_config (
            id      INTEGER PRIMARY KEY CHECK (id = 1),
            hash    BLOB    NOT NULL,
            salt    BLOB    NOT NULL
        )
    """)

    # Bảng lưu mật khẩu (tất cả đã mã hóa AES-256)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            username    TEXT    NOT NULL,
            password    TEXT    NOT NULL,  -- Mã hóa AES-256
            url         TEXT,
            category    TEXT    DEFAULT 'Khác',
            notes       TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ─── Master Config ───────────────────────────────────────────────────────────

def save_master(hashed: bytes, salt: bytes):
    """Lưu hash và salt của Master Password (lần đầu cài đặt)."""
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO master_config (id, hash, salt) VALUES (1, ?, ?)",
        (hashed, salt)
    )
    conn.commit()
    conn.close()


def get_master() -> dict | None:
    """Lấy thông tin master config. Trả về None nếu chưa thiết lập."""
    conn = get_connection()
    row = conn.execute("SELECT hash, salt FROM master_config WHERE id = 1").fetchone()
    conn.close()
    return dict(row) if row else None


# ─── CRUD mật khẩu ──────────────────────────────────────────────────────────

def add_password(title: str, username: str, password_enc: str,
                  url: str = "", category: str = "Khác", notes: str = "") -> int:
    """Thêm một mật khẩu mới. Trả về id vừa tạo."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO passwords (title, username, password, url, category, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, username, password_enc, url, category, notes)
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_all_passwords() -> list[dict]:
    """Lấy tất cả mật khẩu (dạng mã hóa)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM passwords ORDER BY title"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_password_by_id(entry_id: int) -> dict | None:
    """Lấy một mật khẩu theo id."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM passwords WHERE id = ?", (entry_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_password(entry_id: int, title: str, username: str, password_enc: str,
                     url: str = "", category: str = "Khác", notes: str = ""):
    """Cập nhật một mật khẩu."""
    conn = get_connection()
    conn.execute(
        """UPDATE passwords
           SET title=?, username=?, password=?, url=?, category=?, notes=?,
               updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        (title, username, password_enc, url, category, notes, entry_id)
    )
    conn.commit()
    conn.close()


def delete_password(entry_id: int):
    """Xóa một mật khẩu."""
    conn = get_connection()
    conn.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def search_passwords(keyword: str) -> list[dict]:
    """Tìm kiếm mật khẩu theo title, username hoặc url."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT * FROM passwords
           WHERE title LIKE ? OR username LIKE ? OR url LIKE ?
           ORDER BY title""",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
