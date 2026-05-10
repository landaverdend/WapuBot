from __future__ import annotations
import os
import asyncpg
from cryptography.fernet import Fernet

from .session import Session


def _fernet() -> Fernet:
    return Fernet(os.environ["SESSION_ENCRYPTION_KEY"].encode())


def _encrypt(value: str) -> str:
    return _fernet().encrypt(value.encode()).decode()


def _decrypt(value: str) -> str:
    return _fernet().decrypt(value.encode()).decode()


class SessionStore:
    def __init__(self) -> None:
        self._cache: dict[int, Session] = {}
        self._pool: asyncpg.Pool | None = None

    async def init(self, dsn: str) -> None:
        self._pool = await asyncpg.create_pool(dsn)

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    async def get(self, chat_id: int) -> Session:
        if chat_id in self._cache:
            return self._cache[chat_id]

        session = Session(chat_id=chat_id)

        if self._pool:
            row = await self._pool.fetchrow(
                "SELECT email, wapu_api_key_encrypted, ai_api_key_encrypted, ai_model FROM sessions WHERE chat_id = $1",
                chat_id,
            )
            if row:
                session.complete_auth(
                    email=row["email"],
                    wapu_api_key=_decrypt(row["wapu_api_key_encrypted"]),
                )
                if row["ai_api_key_encrypted"]:
                    session.ai_api_key = _decrypt(row["ai_api_key_encrypted"])
                if row["ai_model"]:
                    session.ai_model = row["ai_model"]
                session.dirty = False

        self._cache[chat_id] = session
        return session

    async def save(self, session: Session) -> None:
        if not self._pool or not session.dirty:
            return
        await self._pool.execute(
            """
            INSERT INTO sessions (chat_id, email, wapu_api_key_encrypted, ai_api_key_encrypted, ai_model, updated_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT (chat_id) DO UPDATE SET
                email = EXCLUDED.email,
                wapu_api_key_encrypted = EXCLUDED.wapu_api_key_encrypted,
                ai_api_key_encrypted = EXCLUDED.ai_api_key_encrypted,
                ai_model = EXCLUDED.ai_model,
                updated_at = NOW()
            """,
            session.chat_id,
            session.email,
            _encrypt(session.wapu_api_key),
            _encrypt(session.ai_api_key) if session.ai_api_key else None,
            session.ai_model,
        )
        session.dirty = False
