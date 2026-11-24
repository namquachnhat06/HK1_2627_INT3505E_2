# LAB3/sunset.py — Decorator kiểm soát vòng đời theo chuẩn RFC 8594 & RFC 9110
from datetime import datetime, timezone
from email.utils import format_datetime
from functools import wraps
from flask import request, jsonify
import logging

log = logging.getLogger("sunset")
logging.basicConfig(level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

def http_date(dt):
    """Format datetime sang HTTP-date theo RFC 7231 (Ví dụ: Sat, 31 Dec 2026 23:59:59 GMT)"""
    return format_datetime(dt, usegmt=True)

def deprecate_at(sunset_date, replacement=None):
    """
    Decorator kiểm soát vòng đời API:
    - Nếu now >= sunset_date: Trả về HTTP 410 Gone (Endpoint đã bị tắt hoàn toàn).
    - Nếu now < sunset_date: Trả về kết quả bình thường nhưng gắn kèm các headers:
        + Sunset: thời điểm sẽ tắt (RFC 8594)
        + Deprecation: true (RFC 9110/RFC 9745)
        + Link: </successor>; rel="successor-version"
    - Ghi log warning mỗi lần client gọi tới endpoint cũ.
    """
    def wrap(fn):
        @wraps(fn)
        def inner(*a, **kw):
            now = datetime.now(timezone.utc)
            if now >= sunset_date:
                return jsonify({
                    "error": "gone",
                    "sunset": http_date(sunset_date),
                    "use_instead": replacement
                }), 410
            
            result = fn(*a, **kw)
            body, status = result if isinstance(result, tuple) else (result, 200)
            r = jsonify(body)
            r.status_code = status
            r.headers["Sunset"] = http_date(sunset_date)
            r.headers["Deprecation"] = "true"
            if replacement:
                r.headers["Link"] = f'<{replacement}>; rel="successor-version"'
            log.warning("deprecated_call %s %s", request.path, request.remote_addr)
            return r
        return inner
    return wrap
