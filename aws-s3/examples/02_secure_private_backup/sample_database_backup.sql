-- =============================================================================
-- SAMPLE DATABASE BACKUP DUMP FILE
-- Created for AWS S3 Encrypted Backup Demonstration
-- =============================================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES 
('alice_admin', 'alice@company.com'),
('bob_developer', 'bob@company.com'),
('charlie_user', 'charlie@company.com');

-- Backup completed successfully at 2026-08-25 17:00:00 UTC
