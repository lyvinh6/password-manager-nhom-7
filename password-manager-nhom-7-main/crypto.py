import bcrypt
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def hash_master_password(password: str) -> bytes:
    """Băm Master Password bằng bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_master_password(password: str, hashed: bytes) -> bool:
    """Xác thực Master Password."""
    return bcrypt.checkpw(password.encode(), hashed)

def derive_key(password: str, salt: bytes) -> bytes:
    """Tạo khóa mã hóa AES-256 từ Master Password (Key Derivation)."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt(encrypted_data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()