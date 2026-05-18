from src.config import WEB_AGENT_SYSTEM_MESSAGE
from src.context import create_project_context


def create_web_system_message() -> str:
    project_context = create_project_context()
    return f"""{WEB_AGENT_SYSTEM_MESSAGE}

以下は参考用のプロジェクト情報です。
必要な場合だけ参照してください。

{project_context}
""".strip()


def create_initial_web_conversation_history() -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": create_web_system_message(),
        }
    ]
