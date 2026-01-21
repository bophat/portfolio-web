-- MySQL initialization script
-- This script runs automatically when the MySQL container is first created

-- Ensure the database exists
CREATE DATABASE IF NOT EXISTS portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'%';
FLUSH PRIVILEGES;

-- Use the database
USE portfolio_db;

-- Tables will be created automatically by SQLAlchemy
-- This file can be extended to add additional initialization if needed
