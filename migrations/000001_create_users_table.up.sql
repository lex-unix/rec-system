CREATE TABLE IF NOT EXISTS users (
  id bigserial PRIMARY KEY,
  created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  updated_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  full_name text NOT NULL,
  email text UNIQUE NOT NULL,
  password_hash text NOT NULL
);
