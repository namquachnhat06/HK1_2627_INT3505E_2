# SOA 09 - Practice 3: Sunset Middleware với Decorator @deprecate_at

Dự án minh họa quy trình Deprecation & Sunset theo chuẩn RFC 8594 và RFC 9110 / RFC 9745 trong kiến trúc hướng dịch vụ (SOA).

---

## 1. Mục tiêu bài học
Xây dựng một Decorator tái sử dụng @deprecate_at(sunset_date, replacement=None) để tự động quản lý vòng đời endpoint:
1. Trước ngày Sunset: 
   - Vẫn xử lý request và trả về kết quả bình thường (HTTP 200 OK).
   - Gắn các response headers cảnh báo:
     - Sunset: <HTTP-date> (RFC 8594).
     - Deprecation: true (RFC 9110/9745).
     - Link: </successor>; rel="successor-version".
   - Ghi log cảnh báo mức WARN kèm path và IP client.
2. Sau ngày Sunset:
   - Tự động từ chối request với mã HTTP 410 Gone.
   - Trả về JSON hướng dẫn client chuyển sang endpoint thay thế (use_instead).

---

## 2. Cấu trúc thư mục

```text
LAB3/
├── app.py              # Flask server tích hợp decorator deprecate_at
├── sunset.py           # Sunset middleware / decorator tái sử dụng
├── requirements.txt    # Thư viện phụ thuộc
├── test_api.py         # Script kiểm thử tự động 3 tình huống
└── README.md           # Tài liệu hướng dẫn sử dụng
```

---

## 3. Hướng dẫn chạy và Kiểm thử

### Kích hoạt môi trường ảo (từ thư mục LAB3)
```powershell
cd LAB3
..\venv\Scripts\Activate.ps1
```

### Cách 1: Chạy kiểm thử tự động
```powershell
python test_api.py
```

### Cách 2: Chạy Server và test bằng curl.exe
1. Khởi động server:
   ```powershell
   python app.py
   ```
2. Mở terminal khác và thực thi:

- Tình huống 1: Trước Sunset (HTTP 200 + Headers):
  ```powershell
  curl.exe -i http://localhost:5000/api/v1/users/1
  ```
  Kết quả:
  ```http
  HTTP/1.1 200 OK
  Sunset: Thu, 31 Dec 2026 23:59:59 GMT
  Deprecation: true
  Link: </api/v2/users>; rel="successor-version"
  
  {"id": 1, "full_name": "Nguyễn Văn A"}
  ```

- Tình huống 2: Sau Sunset (HTTP 410 Gone):
  ```powershell
  curl.exe -i http://localhost:5000/api/v0/users/1
  ```
  Kết quả:
  ```http
  HTTP/1.1 410 GONE
  
  {"error": "gone", "sunset": "Wed, 01 Jan 2020 00:00:00 GMT", "use_instead": "/api/v2/users"}
  ```

- Tình huống 3: Gọi phiên bản thay thế v2:
  ```powershell
  curl.exe -i http://localhost:5000/api/v2/users/1
  ```
