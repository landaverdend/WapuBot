from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

from .models import Message
from .session import SessionStore
from .platform import TelegramPlatform
from .handlers import router

load_dotenv()

app = FastAPI()
sessions = SessionStore()
platform = TelegramPlatform(token=os.environ["TELEGRAM_BOT_TOKEN"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != os.environ["WEBHOOK_SECRET"]:
        return PlainTextResponse("Forbidden", status_code=403)

    data = await request.json()

    message_data = data.get("message", {})
    chat_id = message_data.get("chat", {}).get("id")
    text = message_data.get("text", "").strip()
    msg_id = message_data.get("message_id")

    if not chat_id or not text:
        return {"ok": True}

    message = Message(chat_id=chat_id, text=text, message_id=msg_id)
    session = sessions.get(chat_id)
    await router.dispatch(message, session, platform)

    return {"ok": True}
