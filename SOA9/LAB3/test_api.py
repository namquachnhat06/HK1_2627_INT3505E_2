"""
Script kiểm thử tự động cho Practice 3: Sunset Middleware
Chạy độc lập không cần bật web server: python test_api.py
"""
import json
import logging
from app import app

def run_tests():
    client = app.test_client()
    print("=" * 65)
    print("BẮT ĐẦU KIỂM THỬ LAB 3 - SUNSET MIDDLEWARE (@deprecate_at)")
    print("=" * 65)

    # 1. Tình huống 1: Trước Sunset (Endpoint đang được cảnh báo)
    print("\n1. [Tình huống 1: Trước Sunset] GET /api/v1/users/1")
    r1 = client.get("/api/v1/users/1")
    print(f"Status Code: {r1.status_code}")
    print(f"Response Body: {json.dumps(r1.json, ensure_ascii=False)}")
    print(f"Header 'Sunset': {r1.headers.get('Sunset')}")
    print(f"Header 'Deprecation': {r1.headers.get('Deprecation')}")
    print(f"Header 'Link': {r1.headers.get('Link')}")
    
    assert r1.status_code == 200
    assert r1.headers.get("Sunset") == "Thu, 31 Dec 2026 23:59:59 GMT"
    assert r1.headers.get("Deprecation") == "true"
    assert 'rel="successor-version"' in r1.headers.get("Link")
    print("=> PASS: Trước sunset trả về HTTP 200 kèm đầy đủ 3 headers RFC 8594")

    # 2. Tình huống 2: Sau Sunset (Endpoint đã bị khai tử hoàn toàn)
    print("\n2. [Tình huống 2: Sau Sunset] GET /api/v0/users/1")
    r0 = client.get("/api/v0/users/1")
    print(f"Status Code: {r0.status_code}")
    print(f"Response Body: {json.dumps(r0.json, ensure_ascii=False)}")
    
    assert r0.status_code == 410
    assert r0.json.get("error") == "gone"
    assert r0.json.get("use_instead") == "/api/v2/users"
    print("=> PASS: Sau sunset trả về HTTP 410 Gone và hướng dẫn dùng endpoint kế nhiệm")

    # 3. Tình huống 3: Gọi endpoint kế nhiệm v2
    print("\n3. [Tình huống 3: Endpoint kế nhiệm] GET /api/v2/users/1")
    r2 = client.get("/api/v2/users/1")
    print(f"Status Code: {r2.status_code}")
    print(f"Response Body: {json.dumps(r2.json, ensure_ascii=False)}")
    assert r2.status_code == 200
    assert "first_name" in r2.json
    assert "Sunset" not in r2.headers
    print("=> PASS: Endpoint mới v2 hoạt động bình thường, không có cờ deprecation")

    print("\n" + "=" * 65)
    print("TẤT CẢ CÁC TÌNH HUỐNG KIỂM THỬ ĐỀU HOÀN THÀNH XUẤT SẮC (3/3 PASS)!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
