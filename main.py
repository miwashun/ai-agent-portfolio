import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が .env に設定されていません。")

    client = OpenAI(api_key=api_key)

    print("AIエージェントを開始します。終了するには exit または quit と入力してください。")

    while True:
        user_input = input("あなた: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("終了します。")
            break

        if not user_input:
            print("入力が空です。質問を入力してください。")
            continue

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=user_input,
            )
            print(f"AI: {response.output_text}")
        except Exception as error:
            print(f"エラーが発生しました: {error}")


if __name__ == "__main__":
    main()
