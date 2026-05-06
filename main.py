from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)
from src.config import (
    EXIT_COMMANDS,
    MAX_HISTORY_LENGTH,
    PROJECT_CONTEXT_FILES,
    TODO_AGENT_SYSTEM_MESSAGE,
)
from src.openai_client import create_openai_client, generate_ai_response


# プロジェクトコンテキストファイルを読み込む関数
def read_project_context_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"{file_path} は見つかりませんでした。"


# プロジェクトコンテキストを作成する関数
def create_project_context() -> str:
    context_parts = []

    for file_path in PROJECT_CONTEXT_FILES:
        file_content = read_project_context_file(file_path)
        context_parts.append(f"## {file_path}\n\n{file_content}")

    return "\n\n---\n\n".join(context_parts)


# システムメッセージを作成する関数
def create_system_message() -> str:
    project_context = create_project_context()
    return f"""{TODO_AGENT_SYSTEM_MESSAGE}

以下は現在のプロジェクト情報です。
この情報を参考にして、具体的なTODO整理を行ってください。

{project_context}
""".strip()


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


# エラー内容に応じた日本語メッセージを出力する関数
def print_openai_error_message(error: Exception) -> None:
    if isinstance(error, AuthenticationError):
        print("エラー: APIキーが無効、または認証に失敗しました。")
    elif isinstance(error, RateLimitError):
        print("エラー: APIの利用制限に達しました。少し時間をおいてから再実行してください。")
    elif isinstance(error, APITimeoutError):
        print("エラー: APIリクエストがタイムアウトしました。通信環境を確認して再実行してください。")
    elif isinstance(error, APIConnectionError):
        print("エラー: OpenAI APIへの接続に失敗しました。ネットワーク接続を確認してください。")
    elif isinstance(error, NotFoundError):
        print("エラー: モデル名が間違っている可能性があります。MODEL_NAME を確認してください。")
    elif isinstance(error, BadRequestError):
        print("エラー: APIリクエストの内容に問題があります。モデル名や入力形式を確認してください。")
    else:
        print(f"予期しないエラーが発生しました: {error}")


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
