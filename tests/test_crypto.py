"""
Tests cho module crypto.py
[BAO] chạy: python -m pytest tests/
"""

import pytest
from src.core.crypto import (
    hash_master_password,
    verify_master_password,
    derive_key,
    encrypt,
    decrypt,
)


def test_hash_and_verify():
    master = "MyStr0ng!Pass"
    hashed = hash_master_password(master)
    assert verify_master_password(master, hashed) is True
    assert verify_master_password("wrongpass", hashed) is False


def test_encrypt_decrypt():
    import os
    key = os.urandom(32)
    plaintext = "my_secret_password_123"
    encrypted = encrypt(plaintext, key)
    assert encrypted != plaintext
    decrypted = decrypt(encrypted, key)
    assert decrypted == plaintext


def test_derive_key_deterministic():
    import os
    salt = os.urandom(32)
    key1 = derive_key("password", salt)
    key2 = derive_key("password", salt)
    assert key1 == key2
    assert len(key1) == 32  # AES-256 = 32 bytes
