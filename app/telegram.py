from telegram import Bot
import os


async def send_message(chat_id: int | str, text: str) -> None:
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text)


async def send_photo(chat_id: int | str, photo_url: str, caption: str = "") -> None:
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    async with bot:
        await bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)
