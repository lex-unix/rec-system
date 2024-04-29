ALTER TABLE chats
DROP CONSTRAINT chats_issue_id_fkey,
ADD CONSTRAINT chats_issue_id_fkey
FOREIGN KEY (issue_id) REFERENCES issues(id)
ON DELETE CASCADE;
