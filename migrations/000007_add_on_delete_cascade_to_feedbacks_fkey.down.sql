ALTER TABLE feedbacks
DROP CONSTRAINT feedbacks_issue_id_fkey,
ADD CONSTRAINT feedbacks_issue_id_fkey
FOREIGN KEY (issue_id) REFERENCES issues(id)
ON DELETE RESTRICT;
