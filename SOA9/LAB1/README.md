# SOA 09 — Practice 1: URI Path Versioning với Flask Blueprint

Dự án minh họa chiến lược **URI Path Versioning** trong kiến trúc hướng dịch vụ (SOA) và RESTful API, quản lý vòng đời API và xử lý Breaking Change khi nâng cấp từ `v1` lên `v2`.

---

##  Cấu trúc thư mục

```text
SOA9/
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

## ⚙️ Hướng dẫn cài đặt môi trường ảo (venv)

### Bước 1: Mở Terminal
Mở terminal tại thư mục gốc của dự án (`SOA9`). Bạn có thể nhấn phím tắt `` Ctrl + ` `` trong VS Code.

### Bước 2: Tạo môi trường ảo `venv`
Chạy lệnh sau:
```powershell
python -m venv venv
```
*(Sau lệnh này, thư mục `venv/` sẽ được tạo ra).*

### Bước 3: Kích hoạt môi trường ảo

* **Dành cho Windows PowerShell (mặc định trong VS Code)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  > **Lưu ý**: Nếu gặp lỗi `cannot be loaded because running scripts is disabled on this system`, bạn chỉ cần chạy lệnh sau một lần để cấp quyền:
  > ```powershell
  > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  > ```
  > Sau đó chạy lại lệnh kích hoạt `.\venv\Scripts\Activate.ps1`.

* **Dành cho Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

*Khi kích hoạt thành công, bạn sẽ thấy tiền tố `(venv)` xuất hiện ở đầu dòng lệnh trong Terminal.*

### Bước 4: Cài đặt thư viện phụ thuộc
Sau khi đã kích hoạt `(venv)`, chạy lệnh:
```powershell
pip install -r requirements.txt
```

---

##  Hướng dẫn khởi chạy ứng dụng

### 1. Khởi động Flask Server
Chạy lệnh:
```powershell
python app.py
```
Server sẽ chạy tại địa chỉ: `http://127.0.0.1:5000`

### 2. Dừng Server
Nhấn tổ hợp phím `Ctrl + C` trong Terminal.

### 3. Tắt môi trường ảo (khi không làm việc nữa)
Chạy lệnh:
```powershell
deactivate
```

---

##  Hướng dẫn kiểm thử (Testing)

### Cách 1: Chạy script kiểm thử tự động (Nhanh nhất)
Không cần bật server, mở Terminal và chạy:
```powershell
python test_api.py
```
Script sẽ tự động chạy 5 bài kiểm thử:
1. `GET /api/v1/users/1` $\rightarrow$ Trả về `full_name`, kiểm tra headers `Sunset`, `Deprecation`, `Link`.
2. `GET /api/v2/users/1` $\rightarrow$ Trả về `first_name`, `last_name`.
3. `POST /api/v2/users` $\rightarrow$ Tạo user mới với HTTP status `201 Created`.
4. Xác minh user mới tạo hiển thị đúng định dạng trên cả 2 version.
5. Kiểm tra trường hợp user không tồn tại trả về `404 Not Found`.

---

### Cách 2: Kiểm thử thủ công bằng cURL hoặc Trình duyệt

Khi server đang chạy (`python app.py`), bạn có thể mở tab Terminal mới hoặc mở trình duyệt:

#### 1. Kiểm tra API v1 (Legacy Version)
* **Trình duyệt**: Truy cập [http://localhost:5000/api/v1/users/1](http://localhost:5000/api/v1/users/1)
* **cURL**:
  ```powershell
  curl -i http://localhost:5000/api/v1/users/1
  ```
* **Kết quả**:
  ```json
  {
    "id": 1,
    "full_name": "Văn Nguyễn",
    "email": "a@vnu.vn"
  }
  ```
  *Headers trả về có `Sunset: Thu, 31 Dec 2026 23:59:59 GMT` và `Deprecation: true`.*

#### 2. Kiểm tra API v2 (Breaking Change Version)
* **Trình duyệt**: Truy cập [http://localhost:5000/api/v2/users/1](http://localhost:5000/api/v2/users/1)
* **cURL**:
  ```powershell
  curl -i http://localhost:5000/api/v2/users/1
  ```
* **Kết quả**:
  ```json
  {
    "id": 1,
    "first_name": "Văn",
    "last_name": "Nguyễn",
    "email": "a@vnu.vn"
  }
  ```

#### 3. Tạo user mới với API v2 (POST)
* **cURL (PowerShell)**:
  ```powershell
  curl -i -X POST http://localhost:5000/api/v2/users `
    -H "Content-Type: application/json" `
    -d "{\"first_name\": \"Nam\", \"last_name\": \"Quách\", \"email\": \"nam@vnu.vn\"}"
  ```
* **Kết quả**: HTTP `201 Created`
  ```json
  {
    "id": 3,
    "first_name": "Nam",
    "last_name": "Quách",
    "email": "nam@vnu.vn"
  }
  ```

---

##  Tài liệu OpenAPI Spec
File đặc tả chuẩn OpenAPI 3.0 được lưu tại [openapi.yaml](openapi.yaml). Bạn có thể mở file này bằng extension *Swagger Viewer* hoặc dán nội dung vào [editor.swagger.io](https://editor.swagger.io/) để xem giao diện trực quan.
