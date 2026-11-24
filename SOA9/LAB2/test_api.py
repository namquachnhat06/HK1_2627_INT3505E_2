"""
Script kiểm thử tự động cho Practice 2: Header Versioning
Chạy độc lập không cần bật web server: python test_api.py
"""
import json
from app import app

def run_tests():
    client = app.test_client()
    print("=" * 65)
    print("BẮT ĐẦU KIỂM THỬ LAB 2 - HEADER VERSIONING VỚI DECORATOR")
    print("=" * 65)

    # 1. Test Default version (khi không truyền header -> mặc định v2)
    print("\n1. [Default Version] GET /users/1 (Không truyền header)")
    r_default = client.get("/users/1")
    print(f"Status: {r_default.status_code}")
    print(f"Header 'X-API-Version-Served': {r_default.headers.get('X-API-Version-Served')}")
    print(f"Response: {json.dumps(r_default.json, ensure_ascii=False)}")
    assert r_default.status_code == 200
    assert r_default.headers.get("X-API-Version-Served") == "2"
    assert "first_name" in r_default.json and "last_name" in r_default.json
    print("=> PASS: Mặc định rơi vào newest stable (v2)")

    # 2. Test v1 Explicit (Header X-API-Version: 1)
    print("\n2. [v1 Explicit] GET /users/1 kèm header 'X-API-Version: 1'")
    r_v1 = client.get("/users/1", headers={"X-API-Version": "1"})
    print(f"Status: {r_v1.status_code}")
    print(f"Header 'X-API-Version-Served': {r_v1.headers.get('X-API-Version-Served')}")
    print(f"Response: {json.dumps(r_v1.json, ensure_ascii=False)}")
    assert r_v1.status_code == 200
    assert r_v1.headers.get("X-API-Version-Served") == "1"
    assert "full_name" in r_v1.json
    assert r_v1.json["full_name"] == "Văn Nguyễn"
    print("=> PASS: Trả về schema v1 (full_name)")

    # 3. Test Dated version (Header X-API-Version: 2024-06-20)
    print("\n3. [Dated Version] GET /users/1 kèm header 'X-API-Version: 2024-06-20'")
    r_dated = client.get("/users/1", headers={"X-API-Version": "2024-06-20"})
    print(f"Status: {r_dated.status_code}")
    print(f"Header 'X-API-Version-Served': {r_dated.headers.get('X-API-Version-Served')}")
    print(f"Response: {json.dumps(r_dated.json, ensure_ascii=False)}")
    assert r_dated.status_code == 200
    assert r_dated.headers.get("X-API-Version-Served") == "2024-06-20"
    assert "first_name" in r_dated.json and "last_name" in r_dated.json
    print("=> PASS: Hỗ trợ dated version kiểu Stripe")

    # 4. Test Unsupported version (Header X-API-Version: 99 -> HTTP 400)
    print("\n4. [Unsupported Version] GET /users/1 kèm header 'X-API-Version: 99'")
    r_bad = client.get("/users/1", headers={"X-API-Version": "99"})
    print(f"Status: {r_bad.status_code}")
    print(f"Response: {json.dumps(r_bad.json, ensure_ascii=False)}")
    assert r_bad.status_code == 400
    assert r_bad.json.get("error") == "unsupported version"
    print("=> PASS: Version lạ bị từ chối 400 Bad Request, không fallback bậy bạ")

    # 5. Test 404 Not Found
    print("\n5. [User Not Found] GET /users/999")
    r_404 = client.get("/users/999")
    print(f"Status: {r_404.status_code}, Response: {r_404.json}")
    assert r_404.status_code == 404
    print("=> PASS: User không tồn tại trả về 404")

    print("\n" + "=" * 65)
    print("TẤT CẢ CÁC BÀI TEST LAB 2 ĐỀU HOÀN THÀNH XUẤT SẮC (5/5 PASS)!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
