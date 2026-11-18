from flask import Flask
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp

app = Flask(__name__)

# Đăng ký các Blueprint với URL prefix
# Lưu ý quan trọng: Trong Flask, hàm register_blueprint(bp, url_prefix=...) nếu chỉ truyền "/api/v1"
# thì sẽ ghi đè lên url_prefix="/users" định nghĩa ở Blueprint.
# Để tạo đúng URL /api/v1/users/<id> như mục tiêu đề bài, ta cấu hình tiền tố là "/api/v1/users"
# (hoặc có thể dùng lồng Blueprint/Nested Blueprint).
app.register_blueprint(v1_bp, url_prefix="/api/v1/users")
app.register_blueprint(v2_bp, url_prefix="/api/v2/users")

@app.route("/")
def index():
    return {
        "title": "Practice 1 - URI Path Versioning với Flask Blueprint",
        "description": "Hai phiên bản v1 và v2 cùng truy vấn user_id=1 nhưng trả về 2 schema khác nhau.",
        "endpoints": {
            "v1_get_user": "GET /api/v1/users/<id> (Trả về full_name, có kèm Sunset header)",
            "v2_get_user": "GET /api/v2/users/<id> (Trả về first_name, last_name - Breaking change)",
            "v2_create_user": "POST /api/v2/users (Mở rộng: Tạo user mới)",
            "openapi_spec": "Xem file openapi.yaml tại thư mục gốc"
        }
    }

if __name__ == "__main__":
    print("🚀 Server đang khởi động tại http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
