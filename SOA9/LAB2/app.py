# LAB2/app.py — Flask Server hỗ trợ Header Versioning
from flask import Flask
from decorators import api_version
from users_data import get_user

app = Flask(__name__)

@app.route("/users/<int:uid>")
@api_version()
def get_user_endpoint(version, uid):
    u = get_user(uid)
    if not u:
        return {"error": "not found"}, 404
    
    # Version 1: Schema cũ trả về full_name
    if version == "1":
        return {
            "id": uid,
            "full_name": u["f"] + " " + u["l"]
        }
    
    # Version 2 & Dated version ("2024-06-20"): Schema mới tách first_name, last_name
    return {
        "id": uid,
        "first_name": u["f"],
        "last_name": u["l"],
        "email": u["e"]
    }

@app.route("/")
def index():
    return {
        "title": "Practice 2 - Header Versioning với Decorator @api_version",
        "endpoint": "GET /users/<id>",
        "supported_versions": ["1", "2", "2024-06-20"],
        "default_version": "2",
        "usage": "Truyền header 'X-API-Version: <version>' khi gửi request"
    }

if __name__ == "__main__":
    print("🚀 Server LAB 2 đang chạy tại http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
