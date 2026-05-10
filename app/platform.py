from __future__ import annotations
from abc import ABC, abstractmethod
import re


def to_html(text: str) -> str:
    # Telegram HTML supports: b, strong, i, em, u, s, code, pre, a
    # Convert the most common markdown constructs manually
    # Code blocks first (before inline code)
    text = re.sub(r'```(?:\w+)?\n?(.*?)```', lambda m: f'<pre><code>{m.group(1).strip()}</code></pre>', text, flags=re.DOTALL)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Strikethrough
    text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
    # Headers → bold
    text = re.sub(r'^#{1,6}\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    return text


class Platform(ABC):
    @abstractmethod
    async def send_message(self, chat_id: int | str, text: str, html: bool = False) -> None: ...

    @abstractmethod
    async def delete_message(self, chat_id: int | str, message_id: int) -> None: ...


class TelegramPlatform(Platform):
    def __init__(self, token: str) -> None:
        self._token = token

    async def send_message(self, chat_id: int | str, text: str, html: bool = False) -> None:
        from telegram import Bot, constants
        bot = Bot(token=self._token)
        async with bot:
            await bot.send_message(
                chat_id=chat_id,
                text=to_html(text) if html else text,
                parse_mode=constants.ParseMode.HTML if html else None,
            )

    async def delete_message(self, chat_id: int | str, message_id: int) -> None:
        from telegram import Bot
        bot = Bot(token=self._token)
        async with bot:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
