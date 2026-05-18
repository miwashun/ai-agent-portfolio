from src.config import (
    MAX_HISTORY_LENGTH,
)

from src.context import create_system_message


def trim_conversation_history(
    conversation_history: list[dict[str, str]],
) -> list[dict[str, str]]:
    return conversation_history[-MAX_HISTORY_LENGTH:]


# 初期会話履歴を作成する関数
def create_initial_conversation_history() -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": create_system_message(),
        }
    ]
