-- depends: 0002_rename_wapu_key_add_ai_key

ALTER TABLE sessions ADD COLUMN ai_model TEXT NOT NULL DEFAULT 'anthropic/claude-haiku-4-5-20251001';
