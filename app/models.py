from dataclasses import dataclass


@dataclass
class Message:
    chat_id: int
    text: str
    message_id: int
