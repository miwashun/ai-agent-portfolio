from src.config import (
    EXIT_COMMANDS,
    MAX_HISTORY_LENGTH,
)
from src.context import create_system_message
from src.errors import print_openai_error_message
from src.openai_client import create_openai_client, generate_ai_response


def trim_conversation_history(conversation_history: list[dict[str, str]]) -> list[dict[str, str]]:
    return conversation_history[-MAX_HISTORY_LENGTH:]


# 初期会話履歴を作成する関数
def create_initial_conversation_history() -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": create_system_message(),
        }
    ]


# 統計情報を初期化する関数
def create_execution_stats() -> dict[str, int]:
    return {
        "api_success_count": 0,
        "error_count": 0,
    }


# 実行サマリーを表示する関数
def print_execution_summary(stats: dict[str, int]) -> None:
    print("\n実行サマリー:")
    print(f"- API呼び出し成功回数: {stats['api_success_count']}")
    print(f"- エラー回数: {stats['error_count']}")


def run_todo_agent_chat_loop(client) -> None:
    print("AIエージェントを開始します。終了するには exit または quit と入力してください。")
    conversation_history = create_initial_conversation_history()
    stats = create_execution_stats()

    while True:
        user_input = input("あなた: ").strip()

        if user_input.lower() in EXIT_COMMANDS:
            print("終了します。")
            print_execution_summary(stats)
            break

        if not user_input:
            print("入力が空です。質問を入力してください。")
            continue

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history = trim_conversation_history(conversation_history)

        try:
            ai_response = generate_ai_response(client, conversation_history)
            stats["api_success_count"] += 1
            print(f"AI: {ai_response}")
            conversation_history.append({"role": "assistant", "content": ai_response})
            conversation_history = trim_conversation_history(conversation_history)
        except Exception as error:
            stats["error_count"] += 1
            print_openai_error_message(error)


def main() -> None:
    try:
        client = create_openai_client()
        run_todo_agent_chat_loop(client)
    except RuntimeError as error:
        print(f"エラー: {error}")
        print(".env.example を参考に .env を作成してください。")


if __name__ == "__main__":
    main()
