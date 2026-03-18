-- Database setup script
-- Run this to create the database and user

-- Create database (run as postgres superuser)
CREATE DATABASE ide_logs;

-- Connect to the database
\c ide_logs;

-- Create user (optional, for production)
-- CREATE USER ide_logs_user WITH PASSWORD 'your_secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE ide_logs TO ide_logs_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ide_logs_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ide_logs_user;

-- Run the schema
\i schema.sql;
