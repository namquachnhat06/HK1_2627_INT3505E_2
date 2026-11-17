# Phân tích kết quả Load Test (Lab 4)

## 1. Trong 3 kịch bản, kịch bản nào có p95 cao nhất? Vì sao?
- **Kịch bản C** có chỉ số **p95 (Response Time)** cao nhất, xuất hiện hiện tượng tăng vọt (spike) rõ rệt.
- **Nguyên nhân:** Kịch bản C dồn dập 200 người dùng với tốc độ gia tăng (spawn rate) rất lớn (50 users/s). Hệ thống Flask chạy cục bộ và cơ sở dữ liệu SQLite bị nghẽn cổ chai (bottleneck) về tài nguyên CPU cũng như cơ chế khóa ghi dữ liệu, khiến thời gian phản hồi của 95% request tăng đột biến.

## 2. Có endpoint nào fail rate tăng theo số lượng user không? Đoán nguyên nhân dựa trên code.
- **Có**, các endpoint thực hiện ghi dữ liệu như `POST /books` có tỷ lệ fail tăng cao khi số lượng user tăng mạnh ở Kịch bản B và C.
- **Nguyên nhân:** Thao tác `POST` thực hiện ghi dữ liệu xuống database SQLite, gây tranh chấp khóa ghi (write-lock). Khi lượng request đồng thời quá lớn, hệ thống không xử lý kịp dẫn đến timeout hoặc lỗi kết nối.

## 3. Nếu production cần SLO p95 < 300ms, kịch bản nào đạt? Đề xuất baseline cho CI gate.
- **Kịch bản đạt yêu cầu SLO (p95 < 300ms):** Chỉ có **Kịch bản A** (10 users) đáp ứng được ngưỡng an toàn này.
- **Đề xuất baseline cho CI gate:** 
  - Giới hạn số lượng user chạy kiểm thử tự động ở mức **10 đến 20 users** trong vòng 30 giây.
  - Ngưỡng chấp nhận (CI Gate): `Failure rate < 1%` và `p95 Response Time < 300ms`.

---

## Câu hỏi Bonus:
* **Nếu connection pool giới hạn bằng 5, điều gì xảy ra khi 200 user truy cập đồng thời?**
  - Khi connection pool chỉ có 5 kết nối mà có tới 200 user cùng lúc gửi request, 5 request đầu tiên được xử lý, còn 195 request còn lại phải xếp hàng chờ (queue). 
  - Điều này làm thời gian chờ tăng vọt (p95, p99 cực cao) và gây ra lỗi timeout hàng loạt cho người dùng.
* **Làm thế nào để xác nhận bằng Locust?**
  - Quan sát biểu đồ **Total Request Per Second (RPS)** bị bão hòa phẳng ở mức thấp, đồng thời biểu đồ **Response Time** tăng vọt lên hàng nghìn mili-giây, kèm theo tỷ lệ `Failure (%)` tăng cao trong file báo cáo HTML.