from __future__ import annotations
from abc import ABC, abstractmethod


class Platform(ABC):
    @abstractmethod
    async def send_message(self, chat_id: int | str, text: str) -> None: ...

    @abstractmethod
    async def delete_message(self, chat_id: int | str, message_id: int) -> None: ...


class TelegramPlatform(Platform):
    def __init__(self, token: str) -> None:
        self._token = token

    async def send_message(self, chat_id: int | str, text: str) -> None:
        from telegram import Bot
        bot = Bot(token=self._token)
        async with bot:
            await bot.send_message(chat_id=chat_id, text=text)

    async def delete_message(self, chat_id: int | str, message_id: int) -> None:
        from telegram import Bot
        bot = Bot(token=self._token)
        async with bot:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
