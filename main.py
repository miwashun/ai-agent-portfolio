import os
from typing import Any, cast
from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError, AuthenticationError, OpenAI, RateLimitError

MODEL_NAME = "gpt-4.1-mini"
EXIT_COMMANDS = ["exit", "quit"]

MAX_HISTORY_LENGTH = 10
TODO_AGENT_SYSTEM_MESSAGE = """
あなたはTODO整理を支援するAIエージェントです。
ユーザーの入力をもとに、次にやること、優先順位、注意点を整理してください。

制約:
- ファイルを自動編集しない
- Git操作を自動実行しない
- クラウド操作を行わない
- 外部サービスと連携しない
- 実行が必要な操作は、ユーザーが確認して手動で行う前提で提案する
""".strip()


def get_api_key() -> str:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が .env に設定されていません。")

    return api_key


def create_client() -> OpenAI:
    api_key = get_api_key()
    return OpenAI(api_key=api_key)


def get_ai_response(client: OpenAI, conversation_history: list[dict[str, str]]) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=cast(Any, conversation_history),
    )
    return response.output_text



def trim_conversation_history(conversation_history: list[dict[str, str]]) -> list[dict[str, str]]:
    return conversation_history[-MAX_HISTORY_LENGTH:]


# 初期会話履歴を作成する関数
def create_initial_conversation_history() -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": TODO_AGENT_SYSTEM_MESSAGE,
        }
    ]


# 統計情報を初期化する関数
def create_stats() -> dict[str, int]:
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
def print_error_message(error: Exception) -> None:
    if isinstance(error, AuthenticationError):
        print("エラー: APIキーが無効、または認証に失敗しました。")
    elif isinstance(error, RateLimitError):
        print("エラー: APIの利用制限に達しました。少し時間をおいてから再実行してください。")
    elif isinstance(error, APITimeoutError):
        print("エラー: APIリクエストがタイムアウトしました。通信環境を確認して再実行してください。")
    elif isinstance(error, APIConnectionError):
        print("エラー: OpenAI APIへの接続に失敗しました。ネットワーク接続を確認してください。")
    else:
        print(f"予期しないエラーが発生しました: {error}")


def run_chat_loop(client: OpenAI) -> None:
    print("AIエージェントを開始します。終了するには exit または quit と入力してください。")
    conversation_history = create_initial_conversation_history()
    stats = create_stats()

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
            ai_response = get_ai_response(client, conversation_history)
            stats["api_success_count"] += 1
            print(f"AI: {ai_response}")
            conversation_history.append({"role": "assistant", "content": ai_response})
            conversation_history = trim_conversation_history(conversation_history)
        except Exception as error:
            stats["error_count"] += 1
            print_error_message(error)


def main() -> None:
    client = create_client()
    run_chat_loop(client)


if __name__ == "__main__":
    main()
