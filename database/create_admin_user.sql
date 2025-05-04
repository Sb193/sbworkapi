-- Create default admin user
INSERT INTO users (
    username,
    email,
    name,
    password,
    typeUser,
    status
) VALUES (
    'admin',
    'admin@sbwork.com',
    'Admin',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', -- password: admin123
    'ADMIN',
    1
); 