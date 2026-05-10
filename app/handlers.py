import os
from wapu_cli.client import WapuClient, AuthContext
from wapu_cli.errors import WapuCLIError

from .models import Message
from .platform import Platform
from .router import Router
from .session import Session, AWAITING_EMAIL, AWAITING_PASSWORD, AWAITING_AI_KEY, AUTHENTICATED, IDLE

WAPU_BASE_URL = os.environ.get("WAPU_API_BASE_URL", "https://be-prod.wapu.app")

router = Router()


@router.command("/start")
async def start(message: Message, session: Session, platform: Platform) -> None:
    if session.is_authenticated:
        await platform.send_message(message.chat_id, "You're already logged in. Send a message to get started.")
    else:
        await platform.send_message(
            message.chat_id,
            "👋 Welcome to WapuPay bot!\n\nYou're not logged in yet.\n\n/login — connect your Wapu account\n/help — show available commands",
        )


@router.command("/help", description="show this message")
async def help_handler(message: Message, session: Session, platform: Platform) -> None:
    await platform.send_message(message.chat_id, router.help_text())


@router.command("/login", description="connect your Wapu account")
async def login(message: Message, session: Session, platform: Platform) -> None:
    if session.is_authenticated:
        await platform.send_message(message.chat_id, "You're already logged in.")
        return
    session.state = AWAITING_EMAIL
    await platform.send_message(message.chat_id, "Please send your email.")


@router.command("/setkey", description="set your AI API key")
async def setkey(message: Message, session: Session, platform: Platform) -> None:
    if not session.is_authenticated:
        await platform.send_message(message.chat_id, "You need to /login first.")
        return
    session.state = AWAITING_AI_KEY
    await platform.send_message(message.chat_id, "Send your AI API key. It will be deleted from chat immediately.")


@router.command("/cancel", description="cancel current action")
async def cancel(message: Message, session: Session, platform: Platform) -> None:
    session.reset_auth_flow()
    await platform.send_message(message.chat_id, "Cancelled.")


@router.on_state(AWAITING_EMAIL)
async def handle_email(message: Message, session: Session, platform: Platform) -> None:
    session.email = message.text
    session.email_msg_id = message.message_id
    session.state = AWAITING_PASSWORD
    await platform.send_message(message.chat_id, "Enter your password. It will be deleted from the chat history")


@router.on_state(AWAITING_PASSWORD)
async def handle_password(message: Message, session: Session, platform: Platform) -> None:
    email = session.email
    password = message.text

    await platform.delete_message(message.chat_id, message.message_id)
    if session.email_msg_id:
        await platform.delete_message(message.chat_id, session.email_msg_id)

    try:
        unauthenticated = WapuClient(base_url=WAPU_BASE_URL)
        login_payload = unauthenticated.login(email, password)
        access_token = login_payload["access_token"]

        authed = WapuClient(base_url=WAPU_BASE_URL, auth=AuthContext(access_token=access_token))
        wapu_api_key = authed.create_api_token()["token"]
    except (WapuCLIError, KeyError) as e:
        session.reset_auth_flow()
        await platform.send_message(message.chat_id, f"Login failed: {e}\nTry /login again.")
        return

    session.complete_auth(email=email, wapu_api_key=wapu_api_key)
    await platform.send_message(message.chat_id, f"✅ Logged in as {email}.")


@router.on_state(AWAITING_AI_KEY)
async def handle_ai_key(message: Message, session: Session, platform: Platform) -> None:
    await platform.delete_message(message.chat_id, message.message_id)
    session.set_ai_key(message.text)
    session.state = AUTHENTICATED
    await platform.send_message(message.chat_id, "✅ AI API key saved.")


@router.fallback
async def fallback(message: Message, session: Session, platform: Platform) -> None:
    if not session.is_authenticated:
        await platform.send_message(
            message.chat_id,
            "You're not logged in. Use /login to connect your Wapu account.",
        )
        return

    # placeholder — agent will go here
    await platform.send_message(message.chat_id, f"Hola! Recibí tu mensaje: '{message.text}'. El agente estará disponible pronto.")
