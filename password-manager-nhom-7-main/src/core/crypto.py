"""
[BAO] Kiến trúc & Bảo mật
Module xử lý mã hóa AES-256 và hash Master Password.

Thuật toán sử dụng:
- PBKDF2-HMAC-SHA256: Dẫn xuất khóa từ Master Password
- AES-256-GCM: Mã hóa/giải mã dữ liệu mật khẩu
"""

import os
import base64
import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# ─── Hash Master Password ────────────────────────────────────────────────────

def hash_master_password(master_password: str) -> bytes:
    """
    Hash Master Password bằng bcrypt để lưu vào DB.
    Dùng để xác thực khi đăng nhập.
    """
    password_bytes = master_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password_bytes, salt)


def verify_master_password(master_password: str, hashed: bytes) -> bool:
    """Xác thực Master Password nhập vào có khớp với hash đã lưu không."""
    return bcrypt.checkpw(master_password.encode("utf-8"), hashed)


# ─── Dẫn xuất khóa AES từ Master Password ───────────────────────────────────

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Dẫn xuất khóa AES-256 (32 bytes) từ Master Password + salt.
    Dùng PBKDF2-HMAC-SHA256 với 480,000 vòng lặp (khuyến nghị NIST 2023).
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    return kdf.derive(master_password.encode("utf-8"))


# ─── Mã hóa / Giải mã AES-256-GCM ──────────────────────────────────────────

def encrypt(plaintext: str, key: bytes) -> str:
    """
    Mã hóa chuỗi văn bản bằng AES-256-GCM.
    Trả về chuỗi base64: nonce (12 bytes) + ciphertext + tag.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce cho GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    # Ghép nonce + ciphertext để lưu vào DB
    return base64.b64encode(nonce + ciphertext).decode("utf-8")


def decrypt(encrypted_b64: str, key: bytes) -> str:
    """
    Giải mã chuỗi đã mã hóa bằng AES-256-GCM.
    Trả về plaintext gốc.
    """
    raw = base64.b64decode(encrypted_b64)
    nonce = raw[:12]
    ciphertext = raw[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
