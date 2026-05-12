from src.agent import create_initial_conversation_history, trim_conversation_history
from src.openai_client import create_openai_client, generate_ai_response


def generate_chat_reply(message: str) -> str:
    client = create_openai_client()
    conversation_history = create_initial_conversation_history()
    conversation_history.append({"role": "user", "content": message})
    conversation_history = trim_conversation_history(conversation_history)

    return generate_ai_response(client, conversation_history)
