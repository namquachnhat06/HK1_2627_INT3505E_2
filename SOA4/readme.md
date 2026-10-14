# SOA 4 - Tasks API Specification

## 1. Tổng quan dự án
Dự án cung cấp tài liệu đặc tả API cho hệ thống Quản lý Task nội bộ. Hệ thống được thiết kế theo chuẩn kiến trúc RESTful, sử dụng **OpenAPI Specification (OAS) 3.0.3** để tài liệu hóa 5 endpoints cơ bản (List, Get, Create, Patch, Delete). 

Giao diện tài liệu được render trực quan thông qua **Swagger UI** được tích hợp thẳng vào một ứng dụng **Python Flask** cục bộ.

## 2. Hướng dẫn cài đặt và khởi chạy
Yêu cầu hệ thống đã cài đặt Python 3.x.

**Bước 1: Thiết lập môi trường ảo và cài đặt thư viện**
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install flask pyyaml
```

**Bước 2: Khởi chạy server Flask**
```bash
python app.py
```

**Bước 3: Truy cập tài liệu**
* Mở trình duyệt và truy cập: http://127.0.0.1:5000/docs
* Tương tác trực tiếp với API qua nút **"Try it out"**.

---

## 3. Quyết định thiết kế (Design Decisions)

Trong quá trình thiết kế OpenAPI Spec cho Tasks API, nhóm đã cân nhắc và áp dụng 2 quyết định kiến trúc quan trọng sau nhằm đảm bảo tính mở rộng và dễ bảo trì:

### 3.1. Chuẩn hóa phản hồi lỗi theo định dạng RFC 7807 (Problem Details)
Thay vì để mỗi endpoint tự định nghĩa cấu trúc JSON báo lỗi lộn xộn (ví dụ: chỗ trả về `{"error": "..."}`, chỗ lại trả về `{"message": "..."}`), API này được thiết kế tuân thủ nghiêm ngặt chuẩn **RFC 7807**. 

Một `Error` schema duy nhất được định nghĩa tập trung trong block `components/schemas`, chứa đầy đủ các trường tiêu chuẩn: `type`, `title`, `status`, và `detail`. Mọi mã lỗi HTTP như `401 Unauthorized`, `404 Not Found`, hay `422 ValidationError` đều được ánh xạ về cấu trúc thống nhất này. Quyết định này giúp phía Client (Frontend/Mobile) xây dựng được một cơ chế bắt lỗi (Error Handling) chung nhất quán cho toàn bộ hệ thống.

### 3.2. Tối ưu hóa tính tái sử dụng bằng cơ chế `$ref` (Single Source of Truth)
Với một API có nhiều thao tác CRUD, việc lặp lại định nghĩa các object như `Task`, `CreateTaskInput` ở phần Request Body và Response của 5 endpoints khác nhau sẽ khiến file `.yaml` bị phình to và rất rủi ro khi có thay đổi. 

Để giải quyết, toàn bộ định nghĩa cấu trúc dữ liệu, các block phản hồi mẫu (responses) và phương thức xác thực (`bearerAuth`) đều được trừu tượng hóa và chuyển xuống block `components`. Các endpoint ở phần `paths` chỉ việc tham chiếu đến bằng từ khóa `$ref` (ví dụ: `$ref: '#/components/schemas/Task'`). Quyết định này đảm bảo nguyên tắc D.R.Y (Don't Repeat Yourself), nếu sau này cần thêm một trường như `createdAt` vào thực thể Task, lập trình viên chỉ cần sửa đúng ở một dòng duy nhất và toàn bộ hệ thống sẽ tự động đồng bộ.