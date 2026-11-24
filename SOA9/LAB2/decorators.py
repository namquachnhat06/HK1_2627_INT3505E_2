# LAB2/decorators.py — Custom Decorator hỗ trợ Header Versioning
from functools import wraps
from flask import jsonify, request

LATEST = "2"
SUPPORTED = {"1", "2", "2024-06-20"}

def api_version(supported=SUPPORTED, default=LATEST):
    """
    Decorator đọc header X-API-Version:
    1. Nếu client không truyền header -> dùng version mặc định (LATEST = "2").
    2. Nếu version không nằm trong supported -> trả về HTTP 400 'unsupported version'.
    3. Tự động đính kèm header 'X-API-Version-Served' vào response trả về.
    """
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            v = request.headers.get("X-API-Version", default)
            if v not in supported:
                return jsonify(error="unsupported version"), 400
            
            result = fn(v, *args, **kwargs)
            
            # Hỗ trợ cả return dict thông thường và return (dict, status_code)
            if isinstance(result, tuple):
                body, status = result
                response = jsonify(body)
                response.status_code = status
            else:
                response = jsonify(result)
                
            response.headers["X-API-Version-Served"] = v
            return response
        return wrapper
    return decorate
