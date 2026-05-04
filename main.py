
import os
from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError, AuthenticationError, OpenAI, RateLimitError

MODEL_NAME = "gpt-4.1-mini"
EXIT_COMMANDS = ["exit", "quit"]


def get_api_key():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が .env に設定されていません。")

    return api_key


def create_client():
    api_key = get_api_key()
    return OpenAI(api_key=api_key)


def get_ai_response(client, user_input):
    response = client.responses.create(
        model=MODEL_NAME,
        input=user_input,
    )
    return response.output_text


# エラー内容に応じた日本語メッセージを出力する関数
def print_error_message(error):
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


def run_chat_loop(client):
    print("AIエージェントを開始します。終了するには exit または quit と入力してください。")

    while True:
        user_input = input("あなた: ").strip()

        if user_input.lower() in EXIT_COMMANDS:
            print("終了します。")
            break

        if not user_input:
            print("入力が空です。質問を入力してください。")
            continue

        try:
            ai_response = get_ai_response(client, user_input)
            print(f"AI: {ai_response}")
        except Exception as error:
            print_error_message(error)


def main():
    client = create_client()
    run_chat_loop(client)


if __name__ == "__main__":
    main()
