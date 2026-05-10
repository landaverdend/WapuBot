from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from .tools import build_tools

APP_NAME = "wapu_bot"

SYSTEM_PROMPT = (
    "You are WapuBot, an AI payment assistant powered by WapuPay. "
    "Help users manage their Lightning and crypto payments."
)

session_service = InMemorySessionService()


async def chat(chat_id: int, text: str, ai_api_key: str, wapu_api_key: str, model: str) -> str:
    agent = Agent(
        model=LiteLlm(model=model, api_key=ai_api_key),
        name=APP_NAME,
        instruction=SYSTEM_PROMPT,
        tools=build_tools(wapu_api_key),
    )
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    session = await session_service.get_session(
        app_name=APP_NAME, user_id=str(chat_id), session_id=str(chat_id)
    )
    if session is None:
        await session_service.create_session(
            app_name=APP_NAME, user_id=str(chat_id), session_id=str(chat_id)
        )

    message = types.Content(role="user", parts=[types.Part(text=text)])

    response_text = ""
    async for event in runner.run_async(
        user_id=str(chat_id), session_id=str(chat_id), new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text

    return response_text or "..."
