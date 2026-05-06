from src.openai_client import create_openai_client
from src.cli import run_todo_agent_chat_loop


def main() -> None:
    try:
        client = create_openai_client()
        run_todo_agent_chat_loop(client)
    except RuntimeError as error:
        print(f"エラー: {error}")
        print(".env.example を参考に .env を作成してください。")


if __name__ == "__main__":
    main()
