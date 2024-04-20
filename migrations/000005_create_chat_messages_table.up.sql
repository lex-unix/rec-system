CREATE TABLE IF NOT EXISTS chat_messages (
  id bigserial PRIMARY KEY,
  content text NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  chat_id bigserial REFERENCES chats(id) NOT NULL,
  sender_id bigserial REFERENCES users(id) NOT NULL,

  FOREIGN KEY(chat_id) REFERENCES chats(id),
  FOREIGN KEY(sender_id) REFERENCES users(id)
);

