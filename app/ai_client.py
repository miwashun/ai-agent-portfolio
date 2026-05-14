from app.web_context import create_initial_web_conversation_history
from src.agent import trim_conversation_history
from src.openai_client import create_openai_client, generate_ai_response


def generate_chat_reply(messages: list[dict[str, str]]) -> str:
    client = create_openai_client()
    conversation_history = create_initial_web_conversation_history()
    conversation_history.extend(messages)
    conversation_history = trim_conversation_history(conversation_history)

    return generate_ai_response(client, conversation_history)
