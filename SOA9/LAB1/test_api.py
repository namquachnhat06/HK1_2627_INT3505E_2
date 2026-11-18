"""
Script kiểm thử tự động cho Practice 1: URI Path Versioning
Chạy độc lập không cần bật web server: python test_api.py
"""
import json
from app import app

def run_tests():
    client = app.test_client()
    print("=" * 60)
    print("BẮT ĐẦU KIỂM THỬ PRACTICE 1 - URI PATH VERSIONING")
    print("=" * 60)

    # 1. Test GET /api/v1/users/1
    print("\n1. [GET v1] curl http://localhost:5000/api/v1/users/1")
    r1 = client.get("/api/v1/users/1")
    print(f"Status Code: {r1.status_code}")
    print(f"Response Body: {json.dumps(r1.json, ensure_ascii=False, indent=2)}")
    print(f"Header 'Sunset': {r1.headers.get('Sunset')}")
    print(f"Header 'Deprecation': {r1.headers.get('Deprecation')}")
    print(f"Header 'Link': {r1.headers.get('Link')}")
    assert r1.status_code == 200
    assert "full_name" in r1.json
    assert r1.json["full_name"] == "Văn Nguyễn"
    print("=> PASS GET v1")

    # 2. Test GET /api/v2/users/1
    print("\n2. [GET v2] curl http://localhost:5000/api/v2/users/1")
    r2 = client.get("/api/v2/users/1")
    print(f"Status Code: {r2.status_code}")
    print(f"Response Body: {json.dumps(r2.json, ensure_ascii=False, indent=2)}")
    assert r2.status_code == 200
    assert "first_name" in r2.json and "last_name" in r2.json
    assert r2.json["first_name"] == "Văn" and r2.json["last_name"] == "Nguyễn"
    print("=> PASS GET v2 (Schema đổi từ 'full_name' thành 'first_name' + 'last_name')")

    # 3. Test POST /api/v2/users (Mở rộng 1)
    print("\n3. [POST v2] Thêm user mới vào v2")
    payload = {
        "first_name": "Nam",
        "last_name": "Quách Nhật",
        "email": "namqn@vnu.vn"
    }
    r3 = client.post("/api/v2/users", json=payload)
    print(f"Status Code: {r3.status_code}")
    print(f"Response Body: {json.dumps(r3.json, ensure_ascii=False, indent=2)}")
    assert r3.status_code == 201
    new_id = r3.json["id"]
    print("=> PASS POST v2")

    # 4. Kiểm tra user vừa tạo bằng cả 2 version
    print(f"\n4. [Verification] Lấy user id={new_id} vừa tạo qua cả 2 version:")
    check_v1 = client.get(f"/api/v1/users/{new_id}")
    check_v2 = client.get(f"/api/v2/users/{new_id}")
    print(f"  v1 schema: {check_v1.json}")
    print(f"  v2 schema: {check_v2.json}")
    assert check_v1.json["full_name"] == "Nam Quách Nhật"
    assert check_v2.json["first_name"] == "Nam" and check_v2.json["last_name"] == "Quách Nhật"
    print("=> PASS: Cùng một user id chia sẻ dữ liệu nhưng phản hồi đúng schema của từng version!")

    # 5. Test 404
    print("\n5. [GET 404] Truy vấn user không tồn tại:")
    r4 = client.get("/api/v1/users/999")
    print(f"Status Code: {r4.status_code}, Response: {r4.json}")
    assert r4.status_code == 404
    print("=> PASS 404 Not Found")

    print("\n" + "=" * 60)
    print("TẤT CẢ CÁC BÀI TEST ĐỀU HOÀN THÀNH XUẤT SẮC (5/5 PASS)!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
