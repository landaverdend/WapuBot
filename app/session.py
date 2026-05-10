from __future__ import annotations
from dataclasses import dataclass

IDLE = "idle"
AWAITING_EMAIL = "awaiting_email"
AWAITING_PASSWORD = "awaiting_password"
AWAITING_AI_KEY = "awaiting_ai_key"
AUTHENTICATED = "authenticated"


@dataclass
class Session:
    chat_id: int
    state: str = IDLE
    email: str | None = None
    email_msg_id: int | None = None
    wapu_api_key: str | None = None
    ai_api_key: str | None = None
    dirty: bool = False

    @property
    def is_authenticated(self) -> bool:
        return self.state == AUTHENTICATED

    def reset_auth_flow(self) -> None:
        self.state = IDLE
        self.email = None
        self.email_msg_id = None

    def complete_auth(self, email: str, wapu_api_key: str) -> None:
        self.state = AUTHENTICATED
        self.email = email
        self.email_msg_id = None
        self.wapu_api_key = wapu_api_key
        self.dirty = True

    def set_ai_key(self, ai_api_key: str) -> None:
        self.ai_api_key = ai_api_key
        self.dirty = True
