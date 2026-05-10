from __future__ import annotations
from dataclasses import dataclass, field

IDLE = "idle"
AWAITING_EMAIL = "awaiting_email"
AWAITING_PASSWORD = "awaiting_password"
AUTHENTICATED = "authenticated"


@dataclass
class Session:
    chat_id: int
    state: str = IDLE
    email: str | None = None
    email_msg_id: int | None = None
    api_key: str | None = None

    @property
    def is_authenticated(self) -> bool:
        return self.state == AUTHENTICATED

    def reset_auth_flow(self) -> None:
        self.state = IDLE
        self.email = None
        self.email_msg_id = None

    def complete_auth(self, email: str, api_key: str) -> None:
        self.state = AUTHENTICATED
        self.email = email
        self.email_msg_id = None
        self.api_key = api_key


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[int, Session] = {}

    def get(self, chat_id: int) -> Session:
        if chat_id not in self._sessions:
            self._sessions[chat_id] = Session(chat_id=chat_id)
        return self._sessions[chat_id]
