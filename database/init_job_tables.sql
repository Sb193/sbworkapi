-- Select database
USE sbworkdb;

-- Set character set to UTF-8
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS job_tags;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS work_types;
DROP TABLE IF EXISTS recruiter;

-- Create work_types table
CREATE TABLE work_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create locations table
CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create tags table
CREATE TABLE tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create recruiter table
CREATE TABLE recruiter (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    logo_url TEXT,
    background_url TEXT,
    website VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    description TEXT,
    address TEXT,
    location INT,
    company_size ENUM('1-9', '10-49', '50-99', '100-499', '500+'),
    founded_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (location) REFERENCES locations(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create jobs table
CREATE TABLE jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    salary_min INT,
    salary_max INT,
    location_id INT,
    work_type_id INT,
    recruiter_id INT NOT NULL,
    experience_level ENUM('Junior', 'Mid', 'Senior'),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL,
    FOREIGN KEY (work_type_id) REFERENCES work_types(id) ON DELETE SET NULL,
    FOREIGN KEY (recruiter_id) REFERENCES recruiter(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create job_tags table (many-to-many relationship)
CREATE TABLE job_tags (
    job_id INT,
    tag_id INT,
    PRIMARY KEY (job_id, tag_id),
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Insert Work Types
INSERT INTO work_types (name) VALUES
('Remote'),
('Part-time'),
('Full-time');

-- Insert Tags
INSERT INTO tags (name) VALUES
('Java'),
('Python'),
('JavaScript'),
('C++'),
('React'),
('Machine Learning'),
('Data Science'),
('Backend'),
('Frontend'),
('DevOps'),
('AI'),
('Blockchain'),
('Web Development'),
('Mobile Development'),
('Cloud Computing'),
('Project Management'),
('SQL'),
('NoSQL'),
('HTML'),
('CSS');

-- Insert Locations (64 provinces of Vietnam)
INSERT INTO locations (name) VALUES
('Hà Nội'),
('Hồ Chí Minh'),
('Đà Nẵng'),
('Cần Thơ'),
('Hải Phòng'),
('An Giang'),
('Bà Rịa – Vũng Tàu'),
('Bắc Giang'),
('Bắc Kạn'),
('Bạc Liêu'),
('Bắc Ninh'),
('Bến Tre'),
('Bình Dương'),
('Bình Định'),
('Bình Phước'),
('Bình Thuận'),
('Cà Mau'),
('Cao Bằng'),
('Đắk Lắk'),
('Đắk Nông'),
('Điện Biên'),
('Đồng Nai'),
('Đồng Tháp'),
('Gia Lai'),
('Hà Giang'),
('Hà Nam'),
('Hải Dương'),
('Hậu Giang'),
('Hòa Bình'),
('Hưng Yên'),
('Khánh Hòa'),
('Kiên Giang'),
('Kon Tum'),
('Lai Châu'),
('Lâm Đồng'),
('Lạng Sơn'),
('Lào Cai'),
('Long An'),
('Nam Định'),
('Nghệ An'),
('Ninh Bình'),
('Ninh Thuận'),
('Phú Thọ'),
('Phú Yên'),
('Quảng Bình'),
('Quảng Nam'),
('Quảng Ngãi'),
('Quảng Ninh'),
('Quảng Trị'),
('Sóc Trăng'),
('Sơn La'),
('Tây Ninh'),
('Thái Bình'),
('Thái Nguyên'),
('Thanh Hóa'),
('Thừa Thiên-Huế'),
('Tiền Giang'),
('Trà Vinh'),
('Tuyên Quang'),
('Vĩnh Long'),
('Vĩnh Phúc'),
('Yên Bái'); 