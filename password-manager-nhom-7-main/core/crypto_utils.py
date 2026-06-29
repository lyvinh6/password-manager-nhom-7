# File: core/crypto_utils.py
import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoManager:
    @staticmethod
    def generate_salt():
        """Tạo chuỗi Salt ngẫu nhiên (16 bytes)"""
        return os.urandom(16)

    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        """Biến Master Password thành Khóa AES-256 bằng PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # 32 bytes = 256 bit (Dùng cho AES-256)
            salt=salt,
            iterations=600000, # Chạy 600.000 vòng để chống Brute-force
        )
        return kdf.derive(master_password.encode('utf-8'))

    @staticmethod
    def encrypt_data(key: bytes, plaintext_dict: dict):
        """Mã hóa dữ liệu bằng AES-256 GCM (Authenticated Encryption)"""
        aesgcm = AESGCM(key)
        nonce = os.urandom(12) # Sinh IV/Nonce ngẫu nhiên (12 bytes cho GCM)
        
        # Chuyển Dictionary thành chuỗi JSON rồi biến thành bytes
        data_bytes = json.dumps(plaintext_dict).encode('utf-8')
        
        # Tiến hành mã hóa
        ciphertext = aesgcm.encrypt(nonce, data_bytes, None)
        return nonce, ciphertext

    @staticmethod
    def decrypt_data(key: bytes, nonce: bytes, ciphertext: bytes) -> dict:
        """Giải mã dữ liệu, nếu sai mật khẩu hoặc data bị sửa sẽ văng lỗi"""
        aesgcm = AESGCM(key)
        try:
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(decrypted_bytes.decode('utf-8'))
        except Exception:
            # Nếu sai mật khẩu hoặc file bị kẻ gian chỉnh sửa, nó sẽ nhảy vào đây
            return None