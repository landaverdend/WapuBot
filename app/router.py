from __future__ import annotations
from typing import Callable, Awaitable, TYPE_CHECKING

from .models import Message
from .session import Session

if TYPE_CHECKING:
    from .platform import Platform

Handler = Callable[["Message", "Session", "Platform"], Awaitable[None]]


class Router:
    def __init__(self) -> None:
        self._commands: dict[str, Handler] = {}
        self._descriptions: dict[str, str] = {}
        self._state_handlers: dict[str, Handler] = {}
        self._fallback: Handler | None = None

    def command(self, *names: str, description: str = "") -> Callable:
        def decorator(fn: Handler) -> Handler:
            for name in names:
                self._commands[name] = fn
                if description:
                    self._descriptions[name] = description
            return fn
        return decorator

    def help_text(self) -> str:
        return "\n".join(
            f"{name} — {desc}"
            for name, desc in self._descriptions.items()
        )

    def on_state(self, state: str) -> Callable:
        def decorator(fn: Handler) -> Handler:
            self._state_handlers[state] = fn
            return fn
        return decorator

    def fallback(self, fn: Handler) -> Handler:
        self._fallback = fn
        return fn

    async def dispatch(self, message: Message, session: Session, platform: Platform) -> None:
        if message.text in self._commands:
            await self._commands[message.text](message, session, platform)
        elif session.state in self._state_handlers:
            await self._state_handlers[session.state](message, session, platform)
        elif self._fallback:
            await self._fallback(message, session, platform)
