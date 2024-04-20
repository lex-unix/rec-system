CREATE TABLE chats (
  id bigserial PRIMARY KEY,
  created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  issue_id bigint UNIQUE NOT NULL,

  FOREIGN KEY(issue_id) REFERENCES issues(id)
);
