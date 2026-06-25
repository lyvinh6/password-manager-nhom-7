"""
[VINH] Giao diện & Logic
Password Generator - Tạo mật khẩu ngẫu nhiên an toàn.
"""

import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Tạo mật khẩu ngẫu nhiên an toàn bằng secrets module.

    Args:
        length: Độ dài mật khẩu (mặc định 16)
        use_uppercase: Bao gồm chữ hoa
        use_digits: Bao gồm số
        use_symbols: Bao gồm ký tự đặc biệt

    Returns:
        Chuỗi mật khẩu ngẫu nhiên
    """
    alphabet = string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Đảm bảo có ít nhất 1 ký tự của mỗi loại được chọn
    password_chars = []
    if use_uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))

    # Điền phần còn lại
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(alphabet) for _ in range(remaining)]

    # Trộn ngẫu nhiên
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def check_strength(password: str) -> dict:
    """
    Đánh giá độ mạnh của mật khẩu.

    Returns:
        dict với keys: score (0-4), level (str), suggestions (list)
    """
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Độ dài tối thiểu 8 ký tự")

    if len(password) >= 16:
        score += 1

    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Kết hợp chữ hoa và chữ thường")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Thêm ít nhất một chữ số")

    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        suggestions.append("Thêm ký tự đặc biệt (!@#$...)")

    levels = {0: "Rất yếu", 1: "Yếu", 2: "Trung bình", 3: "Mạnh", 4: "Rất mạnh"}
    return {
        "score": score,
        "level": levels.get(score, "Rất yếu"),
        "suggestions": suggestions,
    }
