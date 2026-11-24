# SOA 09 - Practice 1: URI Path Versioning với Flask Blueprint

Dự án minh họa chiến lược URI Path Versioning trong kiến trúc hướng dịch vụ (SOA) và RESTful API, quản lý vòng đời API và xử lý Breaking Change khi nâng cấp từ v1 lên v2.

---

## 1. Cấu trúc thư mục

```text
LAB1/
├── app.py                     # File chính khởi động Flask Server và mount Blueprint
├── openapi.yaml               # Đặc tả OpenAPI 3.0 cho cả 2 version
├── requirements.txt           # Danh sách thư viện phụ thuộc (Flask)
├── test_api.py                # Script kiểm thử tự động (Unit Test / Integration Test)
├── README.md                  # Tài liệu hướng dẫn cài đặt và sử dụng
└── blueprints/
    ├── __init__.py
    ├── users_data.py          # Single source of truth (Dữ liệu người dùng dùng chung)
    ├── v1.py                  # API v1 (Schema cũ: full_name + Sunset header)
    └── v2.py                  # API v2 (Schema mới: first_name, last_name + POST endpoint)
```

---

## 2. Hướng dẫn cài đặt môi trường ảo (venv)

### Bước 1: Mở Terminal
Mở terminal tại thư mục gốc của bài thực hành (SOA9).

### Bước 2: Tạo môi trường ảo venv
Chạy lệnh:
```powershell
python -m venv venv
```

### Bước 3: Kích hoạt môi trường ảo

- Dành cho Windows PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  Lưu ý: Nếu gặp lỗi script bị chặn trên hệ thống, chạy lệnh:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  Sau đó chạy lại lệnh kích hoạt.

- Dành cho Command Prompt (CMD):
  ```cmd
  venv\Scripts\activate.bat
  ```

### Bước 4: Cài đặt thư viện phụ thuộc
Chạy lệnh:
```powershell
pip install -r requirements.txt
```

---

## 3. Hướng dẫn khởi chạy ứng dụng

### Khởi động Flask Server
Chạy lệnh:
```powershell
python app.py
```
Server chạy tại địa chỉ: http://127.0.0.1:5000

### Dừng Server
Nhấn tổ hợp phím Ctrl + C trong Terminal.

### Tắt môi trường ảo
Chạy lệnh:
```powershell
deactivate
```

---

## 4. Hướng dẫn kiểm thử (Testing)

### Cách 1: Chạy script kiểm thử tự động (Khuyên dùng)
Tại thư mục LAB1, chạy:
```powershell
python test_api.py
```
Script tự động kiểm tra 5 kịch bản:
1. GET /api/v1/users/1 -> Trả về full_name, kiểm tra headers Sunset, Deprecation, Link.
2. GET /api/v2/users/1 -> Trả về first_name, last_name.
3. POST /api/v2/users -> Tạo user mới với HTTP status 201 Created.
4. Xác minh user mới tạo hiển thị đúng định dạng trên cả 2 version.
5. Kiểm tra trường hợp user không tồn tại trả về 404 Not Found.

---

### Cách 2: Kiểm thử thủ công bằng curl.exe

Khi server đang chạy (python app.py):

1. Kiểm tra API v1 (Legacy Version):
```powershell
curl.exe -i http://localhost:5000/api/v1/users/1
```
Kết quả:
```json
{
  "id": 1,
  "full_name": "Văn Nguyễn",
  "email": "a@vnu.vn"
}
```
Headers trả về có Sunset: Thu, 31 Dec 2026 23:59:59 GMT và Deprecation: true.

2. Kiểm tra API v2 (Breaking Change Version):
```powershell
curl.exe -i http://localhost:5000/api/v2/users/1
```
Kết quả:
```json
{
  "id": 1,
  "first_name": "Văn",
  "last_name": "Nguyễn",
  "email": "a@vnu.vn"
}
```

3. Tạo user mới với API v2 (POST):
```powershell
curl.exe -i -X POST http://localhost:5000/api/v2/users -H "Content-Type: application/json" -d "{\"first_name\": \"Nam\", \"last_name\": \"Quach\", \"email\": \"nam@vnu.vn\"}"
```
Kết quả: HTTP 201 Created.

---

## 5. Tài liệu OpenAPI Spec
File đặc tả chuẩn OpenAPI 3.0 được lưu tại openapi.yaml.
Giao diện Swagger UI tương tác trực tiếp tại: http://localhost:5000/docs
