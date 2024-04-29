ALTER TABLE chat_messages
DROP CONSTRAINT chat_messages_chat_id_fkey;

ALTER TABLE chat_messages
ADD CONSTRAINT chat_messages_chat_id_fkey
FOREIGN KEY (chat_id) REFERENCES chats(id)
ON DELETE CASCADE;

