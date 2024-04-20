CREATE TABLE IF NOT EXISTS issues (
  id bigserial PRIMARY KEY,
  created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  updated_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
  subject text NOT NULL,
  description text NOT NULL,
  type text NOT NULL,
  status text NOT NULL,
  customer_id bigint NOT NULL,
  operator_id bigint NOT NULL,

  FOREIGN KEY(customer_id) REFERENCES users(id),
  FOREIGN KEY(operator_id) REFERENCES operators(id)
);
