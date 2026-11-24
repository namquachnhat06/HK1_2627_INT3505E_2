# LAB3/app.py — Flask Server tích hợp Sunset Middleware
from datetime import datetime, timezone
from flask import Flask
from sunset import deprecate_at

app = Flask(__name__)

# Ngày Sunset trong tương lai (Client có thời gian để chuyển đổi -> Trả về HTTP 200 + Headers)
V1_SUNSET = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# Ngày Sunset trong quá khứ (Đã hết hạn hỗ trợ -> Tự động trả về HTTP 410 Gone)
V0_SUNSET = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

# 1. Endpoint v1: Đang trong giai đoạn Deprecation (Trước sunset -> HTTP 200 + cảnh báo)
@app.route("/api/v1/users/<int:uid>")
@deprecate_at(V1_SUNSET, replacement="/api/v2/users")
def get_v1(uid):
    return {"id": uid, "full_name": "Nguyễn Văn A"}

# 2. Endpoint v0: Đã quá hạn Sunset (Sau sunset -> HTTP 410 Gone)
@app.route("/api/v0/users/<int:uid>")
@deprecate_at(V0_SUNSET, replacement="/api/v2/users")
def get_v0(uid):
    return {"id": uid, "full_name": "Nguyễn Văn Cũ"}

# 3. Endpoint v2: Phiên bản kế nhiệm (Không bị deprecate)
@app.route("/api/v2/users/<int:uid>")
def get_v2(uid):
    return {
        "id": uid,
        "first_name": "Văn A",
        "last_name": "Nguyễn",
        "email": "vana@vnu.vn"
    }

@app.route("/")
def index():
    return {
        "title": "Practice 3 - Sunset Middleware với Decorator @deprecate_at",
        "endpoints": {
            "v1_before_sunset": "GET /api/v1/users/1 (Trả về HTTP 200 + Headers Sunset, Deprecation, Link)",
            "v0_after_sunset": "GET /api/v0/users/1 (Trả về HTTP 410 Gone)",
            "v2_successor": "GET /api/v2/users/1 (Phiên bản mới kế nhiệm)"
        }
    }

if __name__ == "__main__":
    print("🚀 Server LAB 3 đang chạy tại http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
