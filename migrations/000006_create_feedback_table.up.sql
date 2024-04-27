CREATE TABLE IF NOT EXISTS feedbacks (
  id bigserial PRIMARY KEY,
  created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  updated_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  rating float NOT NULL,
  issue_id bigint UNIQUE NOT NULL,

  FOREIGN KEY(issue_id) REFERENCES issues(id)
);
