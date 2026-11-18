from flask import Blueprint, jsonify
from .users_data import get_user

bp = Blueprint("v1", __name__, url_prefix="/users")

@bp.route("/<int:uid>", methods=["GET"])
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "full_name": f"{u['first_name']} {u['last_name']}",
        "email": u["email"]
    }

# Mở rộng 3: Gắn Sunset header và Deprecation header cho version 1 sắp bị khai tử (RFC 8594)
@bp.after_request
def add_sunset_headers(response):
    response.headers["Sunset"] = "Thu, 31 Dec 2026 23:59:59 GMT"
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/users>; rel="successor-version"'
    return response
