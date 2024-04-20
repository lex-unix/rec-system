CREATE TABLE IF NOT EXISTS operators (
  id bigint PRIMARY KEY REFERENCES users(id),
  rating float DEFAULT 0.0,
  availability boolean DEFAULT TRUE
);
