CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Healthy sample input:
-- users table: 100 records
-- transactions table: 500 records
-- all transaction amounts should be valid positive values

-- Example corrupted input cases:
-- 1. DROP TABLE users;
-- 2. DELETE FROM transactions;
-- 3. UPDATE transactions SET amount = -500 WHERE id % 3 = 0;
-- 4. INSERT INTO users (username, email)
--    SELECT username, email FROM users LIMIT 10;

