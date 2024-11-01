# **Hệ thống Tự Động Crawl Dữ Liệu Từ Báo Mới**

Đây là hệ thống tự động crawl dữ liệu từ trang Báo Mới và lưu trữ vào cơ sở dữ liệu. Hệ thống bao gồm hai phần chính:

1. **Dịch vụ Python (Flask)** để crawl dữ liệu từ Báo Mới.
2. **Dịch vụ Spring Boot** thực hiện tác vụ cronjob, cứ mỗi 5 phút lấy dữ liệu từ dịch vụ Python và lưu vào cơ sở dữ liệu.

---

## **Cấu trúc hệ thống**

- **Python Flask**: Cung cấp API để crawl và trả về dữ liệu từ Báo Mới.
- **Spring Boot**: Thiết lập cronjob để tự động gọi API từ Flask mỗi 5 phút, lấy dữ liệu và lưu vào database.

---

## **Công nghệ sử dụng**

- **Python 3.x với Flask**: Xây dựng dịch vụ API crawl dữ liệu.
- **Java Spring Boot**: Xử lý cronjob và lưu dữ liệu vào database.
- **Database**: PostgreSQL
---

## **Hướng dẫn sử dụng**

- Sử dụng `*category` để lấy danh sách các danh mục (category) từ Báo Mới.
- Sử dụng `*name category` (ví dụ: `*world`, `*society`) để lấy danh sách bài báo tương ứng với category đó.
