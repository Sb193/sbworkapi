# SBWork API

## Giới thiệu
SBWork là một nền tảng kết nối nhà tuyển dụng và ứng viên, cung cấp các tính năng quản lý việc làm, hồ sơ ứng viên và quy trình tuyển dụng.

## Công nghệ sử dụng
- FastAPI
- MySQL
- Redis
- Elasticsearch
- Docker

## Cài đặt và chạy
1. Clone repository
2. Cài đặt Docker và Docker Compose
3. Chạy lệnh:
```bash
# Khởi tạo database
docker cp database/init_db.sql mysql-container:/tmp/init.sql; docker exec -i mysql-container mysql -u root -pSbac@19032003 -e "source /tmp/init.sql"

# Khởi động các service
docker-compose up -d

# Rebuild và khởi động lại các service
docker-compose up --build -d
```

## API Endpoints

### Authentication

#### Đăng ký tài khoản
- **Endpoint**: `POST /api/v1/auth/register`
- **Mô tả**: Tạo tài khoản người dùng mới
- **Request Body**:
```json
{
    "username": "string",        // Tên đăng nhập, tối thiểu 3 ký tự
    "email": "string",          // Email hợp lệ
    "full_name": "string",      // Họ tên đầy đủ
    "password": "string",       // Mật khẩu, tối thiểu 6 ký tự
    "type_user": "ADMIN" | "RECRUITER" | "CANDIDATE"  // Loại người dùng
}
```
- **Response**:
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "type_user": "string",
    "is_active": true,
    "access_token": "string",
    "refresh_token": "string"
}
```
- **Error Cases**:
  - 400 Bad Request: Username đã tồn tại
  - 400 Bad Request: Email đã tồn tại
  - 400 Bad Request: Password không đủ mạnh
  - 400 Bad Request: Type user không hợp lệ

#### Đăng nhập
- **Endpoint**: `POST /api/v1/auth/login`
- **Mô tả**: Đăng nhập vào hệ thống
- **Request Body**:
```json
{
    "username": "string",    // Tên đăng nhập
    "password": "string"     // Mật khẩu
}
```
- **Response**:
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "type_user": "string",
    "is_active": true,
    "access_token": "string",
    "refresh_token": "string"
}
```
- **Error Cases**:
  - 401 Unauthorized: Sai username hoặc password
  - 400 Bad Request: Tài khoản bị khóa

#### Đăng xuất
- **Endpoint**: `POST /api/v1/auth/logout`
- **Mô tả**: Đăng xuất khỏi hệ thống
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "message": "Đăng xuất thành công"
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn

#### Lấy thông tin người dùng
- **Endpoint**: `GET /api/v1/auth/me`
- **Mô tả**: Lấy thông tin người dùng hiện tại
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "type_user": "string",
    "is_active": true
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn

#### Đổi mật khẩu
- **Endpoint**: `POST /api/v1/auth/change-password`
- **Mô tả**: Thay đổi mật khẩu người dùng
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
    "current_password": "string",  // Mật khẩu hiện tại
    "new_password": "string",      // Mật khẩu mới, tối thiểu 6 ký tự
    "confirm_password": "string"   // Xác nhận mật khẩu mới
}
```
- **Response**:
```json
{
    "message": "Đổi mật khẩu thành công"
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 400 Bad Request: Mật khẩu hiện tại không đúng
  - 400 Bad Request: Mật khẩu mới không khớp
  - 400 Bad Request: Mật khẩu mới không đủ mạnh

### Users

#### Lấy danh sách người dùng
- **Endpoint**: `GET /api/v1/users/`
- **Mô tả**: Lấy danh sách người dùng (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `skip`: Số bản ghi bỏ qua (mặc định: 0)
  - `limit`: Số bản ghi trả về (mặc định: 10, tối đa: 100)
  - `email`: Lọc theo email
  - `type_user`: Lọc theo loại người dùng
  - `is_active`: Lọc theo trạng thái hoạt động
- **Response**:
```json
{
    "total": 100,
    "items": [
        {
            "id": 1,
            "username": "string",
            "email": "string",
            "full_name": "string",
            "type_user": "string",
            "is_active": true,
            "created_at": "2024-03-19T00:00:00",
            "updated_at": "2024-03-19T00:00:00"
        }
    ]
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin

#### Lấy thông tin người dùng
- **Endpoint**: `GET /api/v1/users/{user_id}`
- **Mô tả**: Lấy thông tin chi tiết người dùng (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "type_user": "string",
    "is_active": true,
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Người dùng không tồn tại

#### Tạo người dùng
- **Endpoint**: `POST /api/v1/users/`
- **Mô tả**: Tạo người dùng mới (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như đăng ký
- **Response**: Thông tin người dùng đã tạo
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 400 Bad Request: Username/email đã tồn tại

#### Cập nhật người dùng
- **Endpoint**: `PUT /api/v1/users/{user_id}`
- **Mô tả**: Cập nhật thông tin người dùng (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
    "email": "string",          // Email mới
    "full_name": "string",      // Họ tên mới
    "type_user": "string",      // Loại người dùng mới
    "is_active": boolean        // Trạng thái hoạt động
}
```
- **Response**: Thông tin người dùng đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Người dùng không tồn tại
  - 400 Bad Request: Email đã tồn tại

#### Xóa người dùng
- **Endpoint**: `DELETE /api/v1/users/{user_id}`
- **Mô tả**: Xóa người dùng (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Status 204 No Content
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Người dùng không tồn tại

#### Cập nhật thông tin cá nhân
- **Endpoint**: `PUT /api/v1/users/me`
- **Mô tả**: Cập nhật thông tin người dùng hiện tại
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như cập nhật người dùng
- **Response**: Thông tin người dùng đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 400 Bad Request: Email đã tồn tại

### Profiles

#### Lấy danh sách hồ sơ
- **Endpoint**: `GET /api/v1/profiles/`
- **Mô tả**: Lấy danh sách hồ sơ (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `skip`: Số bản ghi bỏ qua (mặc định: 0)
  - `limit`: Số bản ghi trả về (mặc định: 10, tối đa: 100)
  - `email`: Lọc theo email
  - `full_name`: Lọc theo tên
- **Response**:
```json
{
    "total": 100,
    "items": [
        {
            "id": 1,
            "user_id": 1,
            "full_name": "string",
            "email": "string",
            "phone": "string",
            "address": "string",
            "skills": ["string"],
            "created_at": "2024-03-19T00:00:00",
            "updated_at": "2024-03-19T00:00:00"
        }
    ]
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin

#### Lấy thông tin hồ sơ
- **Endpoint**: `GET /api/v1/profiles/{profile_id}`
- **Mô tả**: Lấy thông tin chi tiết hồ sơ (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "id": 1,
    "user_id": 1,
    "full_name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "skills": ["string"],
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Hồ sơ không tồn tại

#### Lấy hồ sơ cá nhân
- **Endpoint**: `GET /api/v1/profiles/me`
- **Mô tả**: Lấy hồ sơ của người dùng hiện tại
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Tương tự như lấy thông tin hồ sơ
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 404 Not Found: Chưa có hồ sơ

#### Tạo hồ sơ
- **Endpoint**: `POST /api/v1/profiles/`
- **Mô tả**: Tạo hồ sơ mới
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
    "full_name": "string",    // Họ tên đầy đủ
    "email": "string",        // Email liên hệ
    "phone": "string",        // Số điện thoại
    "address": "string",      // Địa chỉ
    "skills": ["string"]      // Danh sách kỹ năng
}
```
- **Response**: Thông tin hồ sơ đã tạo
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 400 Bad Request: Email đã tồn tại
  - 400 Bad Request: Đã có hồ sơ

#### Cập nhật hồ sơ
- **Endpoint**: `PUT /api/v1/profiles/{profile_id}`
- **Mô tả**: Cập nhật thông tin hồ sơ (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như tạo hồ sơ
- **Response**: Thông tin hồ sơ đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Hồ sơ không tồn tại
  - 400 Bad Request: Email đã tồn tại

#### Cập nhật hồ sơ cá nhân
- **Endpoint**: `PUT /api/v1/profiles/me`
- **Mô tả**: Cập nhật hồ sơ của người dùng hiện tại
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như tạo hồ sơ
- **Response**: Thông tin hồ sơ đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 404 Not Found: Chưa có hồ sơ
  - 400 Bad Request: Email đã tồn tại

#### Xóa hồ sơ
- **Endpoint**: `DELETE /api/v1/profiles/{profile_id}`
- **Mô tả**: Xóa hồ sơ (chỉ admin)
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Status 204 No Content
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không có quyền admin
  - 404 Not Found: Hồ sơ không tồn tại

### Jobs

#### Lấy danh sách việc làm
- **Endpoint**: `GET /api/v1/jobs/`
- **Mô tả**: Lấy danh sách việc làm
- **Query Parameters**:
  - `skip`: Số bản ghi bỏ qua (mặc định: 0)
  - `limit`: Số bản ghi trả về (mặc định: 10, tối đa: 100)
  - `location_id`: Lọc theo địa điểm
  - `work_type_id`: Lọc theo loại hình công việc
  - `experience_level`: Lọc theo mức kinh nghiệm
  - `industry`: Lọc theo ngành nghề
  - `salary_min`: Lọc theo mức lương tối thiểu
  - `salary_max`: Lọc theo mức lương tối đa
- **Response**:
```json
{
    "total": 100,
    "items": [
        {
            "id": 1,
            "title": "string",
            "description": "string",
            "salary_min": 10000000,
            "salary_max": 20000000,
            "location_id": 1,
            "work_type_id": 1,
            "experience_level": "string",
            "industry": "string",
            "recruiter_id": 1,
            "created_at": "2024-03-19T00:00:00",
            "updated_at": "2024-03-19T00:00:00"
        }
    ]
}
```

#### Lấy thông tin việc làm
- **Endpoint**: `GET /api/v1/jobs/{job_id}`
- **Mô tả**: Lấy thông tin chi tiết việc làm
- **Response**:
```json
{
    "id": 1,
    "title": "string",
    "description": "string",
    "salary_min": 10000000,
    "salary_max": 20000000,
    "location_id": 1,
    "work_type_id": 1,
    "experience_level": "string",
    "industry": "string",
    "recruiter_id": 1,
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```
- **Error Cases**:
  - 404 Not Found: Việc làm không tồn tại

#### Tạo việc làm
- **Endpoint**: `POST /api/v1/jobs/`
- **Mô tả**: Tạo việc làm mới (chỉ recruiter)
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
    "title": "string",            // Tiêu đề việc làm
    "description": "string",      // Mô tả chi tiết
    "salary_min": number,         // Mức lương tối thiểu
    "salary_max": number,         // Mức lương tối đa
    "location_id": number,        // ID địa điểm
    "work_type_id": number,       // ID loại hình công việc
    "experience_level": "string", // Mức kinh nghiệm
    "industry": "string"          // Ngành nghề
}
```
- **Response**: Thông tin việc làm đã tạo
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter
  - 400 Bad Request: Thiếu thông tin bắt buộc
  - 404 Not Found: Location/Work type không tồn tại

#### Cập nhật việc làm
- **Endpoint**: `PUT /api/v1/jobs/{job_id}`
- **Mô tả**: Cập nhật thông tin việc làm (chỉ recruiter)
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như tạo việc làm
- **Response**: Thông tin việc làm đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter hoặc không sở hữu việc làm
  - 404 Not Found: Việc làm không tồn tại
  - 400 Bad Request: Thiếu thông tin bắt buộc

#### Xóa việc làm
- **Endpoint**: `DELETE /api/v1/jobs/{job_id}`
- **Mô tả**: Xóa việc làm (chỉ recruiter)
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Status 204 No Content
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter hoặc không sở hữu việc làm
  - 404 Not Found: Việc làm không tồn tại

### Recruiters

#### Lấy thông tin nhà tuyển dụng
- **Endpoint**: `GET /api/v1/recruiters/me`
- **Mô tả**: Lấy thông tin nhà tuyển dụng hiện tại
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "id": 1,
    "user_id": 1,
    "name": "string",
    "slug": "string",
    "website": "string",
    "email": "string",
    "phone": "string",
    "description": "string",
    "address": "string",
    "location": "string",
    "company_size": "string",
    "founded_year": 2020,
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter
  - 404 Not Found: Chưa có hồ sơ nhà tuyển dụng

#### Tạo hồ sơ nhà tuyển dụng
- **Endpoint**: `POST /api/v1/recruiters/`
- **Mô tả**: Tạo hồ sơ nhà tuyển dụng
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
    "name": "string",            // Tên công ty
    "slug": "string",            // Slug URL
    "website": "string",         // Website công ty
    "email": "string",           // Email liên hệ
    "phone": "string",           // Số điện thoại
    "description": "string",     // Mô tả công ty
    "address": "string",         // Địa chỉ
    "location": "string",        // Vị trí
    "company_size": "1-9" | "10-49" | "50-99" | "100-499" | "500+",  // Quy mô công ty
    "founded_year": number       // Năm thành lập
}
```
- **Response**: Thông tin nhà tuyển dụng đã tạo
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter
  - 400 Bad Request: Email đã tồn tại
  - 400 Bad Request: Đã có hồ sơ nhà tuyển dụng

#### Cập nhật hồ sơ nhà tuyển dụng
- **Endpoint**: `PUT /api/v1/recruiters/me`
- **Mô tả**: Cập nhật hồ sơ nhà tuyển dụng
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Tương tự như tạo hồ sơ
- **Response**: Thông tin nhà tuyển dụng đã cập nhật
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter
  - 404 Not Found: Chưa có hồ sơ nhà tuyển dụng
  - 400 Bad Request: Email đã tồn tại

#### Xóa hồ sơ nhà tuyển dụng
- **Endpoint**: `DELETE /api/v1/recruiters/me`
- **Mô tả**: Xóa hồ sơ nhà tuyển dụng
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Status 204 No Content
- **Error Cases**:
  - 401 Unauthorized: Token không hợp lệ hoặc hết hạn
  - 403 Forbidden: Không phải recruiter
  - 404 Not Found: Chưa có hồ sơ nhà tuyển dụng

## Cấu trúc dự án
```
app/
├── core/           # Các module cốt lõi
├── db/             # Kết nối database
├── models/         # SQLAlchemy models
├── routers/        # API routes
├── schemas/        # Pydantic models
└── services/       # Business logic
```

## Quy ước đặt tên
- Tên file: snake_case
- Tên class: PascalCase
- Tên biến: snake_case
- Tên hàm: snake_case

## Quy ước commit
- feat: Thêm tính năng mới
- fix: Sửa lỗi
- docs: Cập nhật tài liệu
- style: Cập nhật định dạng
- refactor: Tái cấu trúc code
- test: Thêm test
- chore: Cập nhật cấu hình

## Quy ước code
- Sử dụng type hints
- Viết docstring cho các hàm
- Sử dụng black để format code
- Sử dụng isort để sắp xếp imports
- Sử dụng flake8 để kiểm tra lỗi

## License
MIT