
# Phân Tích Ảnh Hưởng Của Thời Tiết Đến Đánh Giá Nhà Hàng Từ Yelp

## Mục tiêu

Dự án này nhằm phân tích tác động của điều kiện thời tiết (mưa và nhiệt độ) tới đánh giá khách hàng cho các nhà hàng tại bang Nevada (Mỹ), sử dụng dữ liệu từ Yelp và nguồn thời tiết GHCN-D. Mục tiêu cuối cùng là phần nào rút ra các insight vận hành hoặc gợi ý chiến lược phù hợp với biến động thời tiết.

---

## Dữ liệu sử dụng

- **Dữ liệu Yelp:**
  - `business.json`: Thông tin nhà hàng (ID, tên, địa điểm, category…)
  - `review.json`: Các đánh giá từ người dùng (ngày, sao, nội dung…)
  - `user.json`: Thông tin người dùng
- **Dữ liệu thời tiết (GHCN-D):**
  - Bao gồm **nhiệt độ** và **lượng mưa hàng ngày** tại bang Nevada (Las Vegas)

---

## Công cụ sử dụng

- Python (Pandas, SQLAlchemy)
- PostgreSQL (chạy bằng Docker)
- dbt (data modeling)
- Power BI *(xem ghi chú bên dưới)*

---

## Kiến trúc & luồng xử lý dữ liệu

```plaintext
[Yelp JSON]           [Thời tiết CSV]
     │                      │
     ▼                      ▼
    Python làm sạch & chuẩn hóa (pandas)
     │                      │
     └───── Join theo ngày đánh giá ─────┘
                     ▼
    PostgreSQL (chạy trong Docker container)
                     ▼
     dbt xử lý:
     - staging: chuẩn hóa schema
     - mart: làm bảng tổng hợp tính toán & logic cuối phục vụ phân tích và trực quan hoá
```

**Docker setup:**  
PostgreSQL được khởi tạo trong Docker container kèm volume mount & network.  
Thông tin kết nối được quản lý qua biến môi trường (`.env`) và `profiles.yml` của dbt.

---

## Định hướng phân tích *(chưa triển khai đầy đủ do giới hạn thời gian)*

- Ảnh hưởng của mưa đến đánh giá: so sánh `avg_reviews` giữa ngày mưa và không mưa
- Tác động của nhiệt độ: phân loại nhiệt độ theo nhóm (nóng, lạnh, cực đoan…)
- Tính chênh lệch điểm số giữa mưa và không mưa theo từng nhà hàng
- Phân tích theo loại hình nhà hàng: ví dụ `Cafe`, `Fast Food`, `Fine Dining`...
- Phân tích cảm xúc: xử lý text review để xác định xu hướng cảm xúc theo thời tiết

---

## Power BI Dashboard

File Power BI `.pbix` đã được kết nối thành công với cơ sở dữ liệu PostgreSQL chứa bảng dữ liệu và sẵn sàng cho phân tích. Tuy nhiên, do giới hạn thời gian, phần trực quan hóa dashboard chưa được hoàn thiện.


---

## Tài liệu nộp kèm

| Mục                    | Ghi chú                                                   |
|------------------------|-----------------------------------------------------------|
| `/raw_scripts/`        | Script xử lý dữ liệu raw từ Yelp & thời tiết              |
| `/models/`             | File dbt: staging & mart                                  |
| `README.md`            | Mô tả dự án và kiến trúc tổng quan                        |
| `Yelp_Climate_Dashboard.pbix` | Đã kết nối dữ liệu                                 |
