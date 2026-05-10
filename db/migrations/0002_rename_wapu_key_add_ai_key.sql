-- depends: 0001_create_sessions

ALTER TABLE sessions RENAME COLUMN api_key_encrypted TO wapu_api_key_encrypted;
ALTER TABLE sessions ADD COLUMN ai_api_key_encrypted TEXT;
