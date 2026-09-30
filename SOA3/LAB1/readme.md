# Thiết kế Resource cho Blog API

1. Xác định resources trong miền
Dựa trên bài toán nền tảng blog cơ bản, chúng ta xác định được các thực thể (resources) chính cần quản lý bao gồm[cite: 9]:
* **Users**: Người dùng hệ thống, bao gồm hồ sơ cá nhân và chức năng theo dõi (follow) tác giả khác[cite: 9].
* **Posts**: Các bài viết được người dùng đăng tải[cite: 9].
* **Comments**: Các bình luận tương tác bên dưới mỗi bài viết[cite: 9].
* **Tags**: Các thẻ phân loại được gắn vào bài viết để dễ dàng tìm kiếm[cite: 9].

2. Phân loại collection / item / sub-resource
Áp dụng nguyên tắc thiết kế RESTful, các tài nguyên được phân loại và định tuyến như sau[cite: 9]:

Thực thể Users
* **Collection:** `/users` (Danh sách toàn bộ người dùng)
* **Item:** `/users/{user_id}` (Hồ sơ chi tiết của một người dùng cụ thể)
* **Sub-resource (Follow):** 
  * `/users/{user_id}/followers` (Danh sách những người đang theo dõi user này)
  * `/users/{user_id}/following` (Danh sách những người mà user này đang theo dõi)

Thực thể Posts
* **Collection:** `/posts` (Danh sách bài viết)[cite: 9]
* **Item:** `/posts/{post_id}` (Chi tiết một bài viết)
* **Sub-resource (Comments):** `/posts/{post_id}/comments` (Danh sách bình luận của riêng bài viết đó)[cite: 9]
* **Sub-resource (Tags):** `/posts/{post_id}/tags` (Danh sách các thẻ được gắn vào bài viết)[cite: 9]

* **Collection:** `/tags`
* **Item:** `/tags/{tag_id}`

3. Quyết định version segment và Sơ đồ cây endpoint
**Version Segment:** Lựa chọn sử dụng tiền tố `/api/v1` cho toàn bộ các endpoint[cite: 9]. Việc này giúp hệ thống dễ dàng nâng cấp lên `v2`, `v3` trong tương lai mà không làm gián đoạn các ứng dụng client đang sử dụng phiên bản cũ.

**Sơ đồ cây endpoint chi tiết:**
```text
/api/v1
├── /users
│   └── /{user_id}
│       ├── /followers
│       └── /following
├── /posts
│   └── /{post_id}
│       ├── /comments
│       │   └── /{comment_id}
│       └── /tags
└── /tags
    └── /{tag_id}