# Báo cáo Kiểm toán Bảo mật API (Security Audit)

Dựa trên cấu trúc API mạng xã hội và các nguyên tắc bảo mật (OWASP API Security Top 10), dưới đây là 5 điểm yếu (vulnerabilities) có thể dẫn đến việc lộ lọt dữ liệu hoặc xâm nhập hệ thống:

### 1. BOLA (Broken Object Level Authorization) trên `GET /posts/{id}`
*   **Mô tả:** Mặc dù user đã gửi JWT hợp lệ và có scope `posts:read`, nhưng nếu hệ thống không kiểm tra quyền sở hữu (ownership) đối với tham số `{id}`, User A có thể truyền ID bài viết nháp (draft) hoặc bài viết riêng tư (private) của User B để đọc trộm[cite: 36].
*   **Khắc phục:** Cần thêm middleware/policy để kiểm tra quyền truy cập ở cấp độ đối tượng (VD: `if post.is_private and post.author_id != current_user.id: return 403`)[cite: 38].

### 2. Không thu hồi phiên hoặc Refresh Token khi đăng xuất (Session Revocation Failure)
*   **Mô tả:** JWT là token dạng stateless (tự chứa trạng thái)[cite: 25]. Nếu thiết kế tính năng Logout (Đăng xuất) chỉ đơn thuần là xóa token ở localStorage của client mà không ghi nhận `jti` (JWT ID) vào blocklist (ví dụ: dùng Redis) ở phía server, token bị lộ đó vẫn có thể được kẻ tấn công tái sử dụng cho đến khi hết hạn (exp)[cite: 27].
*   **Khắc phục:** Thiết lập blocklist ở Backend, khi logout hoặc khi khóa tài khoản phải chặn cả Access Token và Refresh Token[cite: 27].

### 3. Rủi ro lộ lọt thông tin (PII) trong Payload của JWT
*   **Mô tả:** JWT dạng JWS compact chỉ được ký (signature) chứ không được mã hóa (encrypted)[cite: 26]. Payload là Base64URL nên ai cũng có thể decode được[cite: 26]. Nếu nhúng thông tin nhạy cảm (mật khẩu, email cá nhân, số điện thoại) vào claims của JWT[cite: 30], thông tin này sẽ bị lộ nếu token rơi vào tay người khác.
*   **Khắc phục:** Chỉ đưa các thông tin định danh tối thiểu (VD: `sub` chứa user_id, `roles`, `scopes`) vào payload của token[cite: 30].

### 4. Tấn công vét cạn mật khẩu (Credential Stuffing / Brute Force) ở `POST /auth/login`
*   **Mô tả:** Endpoint `/auth/login` nếu không được giới hạn tốc độ (rate-limit), kẻ tấn công có thể dùng công cụ tự động để thử hàng ngàn tổ hợp email/mật khẩu bị rò rỉ từ các vụ hack khác để đăng nhập trái phép[cite: 41]. 
*   **Khắc phục:** Áp dụng rate-limit nghiêm ngặt cho endpoint login (ví dụ: tối đa 5 lần thử sai trong 15 phút), trả về chung một thông báo lỗi "Sai email hoặc mật khẩu" thay vì phân biệt rõ là sai cái nào, và tránh dùng các hàm hash quá nhanh (nên dùng Argon2id hoặc bcrypt có cost phù hợp)[cite: 39, 41].

### 5. Rủi ro XSS khi lưu JWT sai cách ở Client (Local Storage)
*   **Mô tả:** Frontend SPA lưu trữ JWT Access Token trong `localStorage`. Bất kỳ mã JavaScript độc hại nào chạy trên trang (thông qua tấn công XSS) cũng có thể đọc được `document.localStorage.getItem('token')` và đánh cắp token của người dùng[cite: 30].
*   **Khắc phục:** Nên cân nhắc mô hình BFF (Backend For Frontend) lưu token trong cookie có set cờ `HttpOnly` và `Secure` để ngăn JavaScript truy cập, hoặc áp dụng các biện pháp chặn XSS chặt chẽ[cite: 30].