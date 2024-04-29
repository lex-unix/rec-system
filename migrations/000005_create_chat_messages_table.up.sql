CREATE TABLE IF NOT EXISTS chat_messages (
  id bigserial PRIMARY KEY,
  content text NOT NULL,
  created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  chat_id bigint REFERENCES chats(id) NOT NULL,
  sender_id bigint REFERENCES users(id) NOT NULL
);

