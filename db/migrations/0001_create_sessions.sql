-- depends:

CREATE TABLE sessions (
    id                BIGSERIAL PRIMARY KEY,
    chat_id           BIGINT UNIQUE NOT NULL,
    email             TEXT NOT NULL,
    api_key_encrypted TEXT NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
