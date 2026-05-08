from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

from .telegram import send_message

load_dotenv()

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != os.environ["WEBHOOK_SECRET"]:
        return PlainTextResponse("Forbidden", status_code=403)

    data = await request.json()

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return {"ok": True}

    # placeholder — agent will go here
    reply = f"Hola! Recibí tu mensaje: '{text}'. El agente estará disponible pronto."
    await send_message(chat_id, reply)

    return {"ok": True}
