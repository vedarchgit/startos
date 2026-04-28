-- STRATOS-DB: Run only to create DB/user if needed.
-- SQLAlchemy handles all table creation via /setup route.
-- Usage: sudo mariadb < database/init.sql

CREATE DATABASE IF NOT EXISTS stratos_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Replace 'ved' and 'yourpassword' with your actual username/password
-- GRANT ALL PRIVILEGES ON stratos_db.* TO 'ved'@'127.0.0.1' IDENTIFIED BY 'yourpassword';
-- FLUSH PRIVILEGES;
