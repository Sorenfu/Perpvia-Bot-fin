CREATE TABLE IF NOT EXISTS daily_checkins(
id SERIAL PRIMARY KEY,
user_id BIGINT,
reward INT,
created_at TIMESTAMP DEFAULT NOW()
);
