# LAB2/users_data.py — Tầng lưu trữ dữ liệu người dùng dùng chung

USERS = {
    1: {"f": "Văn", "l": "Nguyễn", "e": "a@vnu.vn"},
    2: {"f": "Trang", "l": "Trần", "e": "b@vnu.vn"}
}

def get_user(uid: int):
    """Lấy thông tin người dùng theo ID"""
    return USERS.get(uid)
