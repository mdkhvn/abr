CREATE TABLE IF NOT EXISTS mysql_logs (
    id SERIAL PRIMARY KEY,
    log_time TIMESTAMP,
    host TEXT,
    severity TEXT,
    message TEXT
);