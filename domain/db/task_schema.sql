BEGIN;

CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,                         -- identifier
  title VARCHAR(200) NOT NULL,                   -- task title
  description TEXT,                              -- optional details
  status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending | in_progress | done
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),   -- created timestamp
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),   -- last updated timestamp
  CONSTRAINT tasks_status_check CHECK (status IN ('pending','in_progress','done'))
);

-- Keep updated_at in sync automatically on updates
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_tasks_set_updated_at ON tasks;
CREATE TRIGGER trg_tasks_set_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMIT;
