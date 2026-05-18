from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)


def print_openai_error_message(error: Exception) -> None:
    if isinstance(error, AuthenticationError):
        print("エラー: APIキーが無効、または認証に失敗しました。")
    elif isinstance(error, RateLimitError):
        print(
            "エラー: APIの利用制限に達しました。少し時間をおいてから再実行してください。"
        )
    elif isinstance(error, APITimeoutError):
        print(
            "エラー: APIリクエストがタイムアウトしました。通信環境を確認して再実行してください。"
        )
    elif isinstance(error, APIConnectionError):
        print(
            "エラー: OpenAI APIへの接続に失敗しました。ネットワーク接続を確認してください。"
        )
    elif isinstance(error, NotFoundError):
        print(
            "エラー: モデル名が間違っている可能性があります。MODEL_NAME を確認してください。"
        )
    elif isinstance(error, BadRequestError):
        print(
            "エラー: APIリクエストの内容に問題があります。モデル名や入力形式を確認してください。"
        )
    else:
        print(f"予期しないエラーが発生しました: {error}")
