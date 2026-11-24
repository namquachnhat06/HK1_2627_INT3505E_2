# SOA 09 - Practice 2: Header Versioning với Decorator @api_version

Dự án minh họa chiến lược Header Versioning (Custom Header Pattern) trong kiến trúc hướng dịch vụ (SOA).

---

## 1. Mục tiêu bài học
- Cùng một URL duy nhất (GET /users/{id}) phục vụ cho cả 3 phiên bản API (1, 2, 2024-06-20).
- Client lựa chọn phiên bản thông qua HTTP Header: X-API-Version.
- Server tự động gắn Header X-API-Version-Served vào response để hỗ trợ debug và đo lường metric.

---

## 2. Bốn điểm cần nhớ (Slide 21)
1. Decorator parse X-API-Version: Nếu request thiếu header -> tự động dùng version mặc định (LATEST = "2").
2. Trả header X-API-Version-Served: Giúp client và công cụ observability biết chính xác version nào đã xử lý request.
3. Endpoint trả schema linh hoạt theo version:
   - Version 1: full_name
   - Version 2 và 2024-06-20: first_name, last_name, email
4. Version không được hỗ trợ -> Trả về HTTP 400: Không tự ý fallback để tránh client hiểu sai dữ liệu.

---

## 3. Cấu trúc thư mục

```text
LAB2/
├── app.py              # Flask server định nghĩa endpoint GET /users/<uid>
├── decorators.py       # Custom decorator @api_version
├── users_data.py       # Tầng lưu trữ dữ liệu người dùng
├── requirements.txt    # Thư viện phụ thuộc
├── test_api.py         # Script kiểm thử tự động 5 kịch bản
└── README.md           # Hướng dẫn chi tiết
```

---

## 4. Hướng dẫn chạy và Kiểm thử

### Cách 1: Chạy test tự động (Khuyên dùng)
Tại thư mục LAB2, chạy lệnh:
```powershell
python test_api.py
```

### Cách 2: Chạy server và test bằng curl.exe
1. Khởi động server:
   ```powershell
   python app.py
   ```
2. Mở terminal mới và thực thi các câu lệnh test:

- Mặc định (Không truyền header -> nhận v2):
  ```powershell
  curl.exe -i http://localhost:5000/users/1
  ```
- Chỉ định v1:
  ```powershell
  curl.exe -i -H "X-API-Version: 1" http://localhost:5000/users/1
  ```
- Chỉ định version theo ngày (Dated version):
  ```powershell
  curl.exe -i -H "X-API-Version: 2024-06-20" http://localhost:5000/users/1
  ```
- Truyền version không hỗ trợ (-> HTTP 400):
  ```powershell
  curl.exe -i -H "X-API-Version: 99" http://localhost:5000/users/1
  ```
