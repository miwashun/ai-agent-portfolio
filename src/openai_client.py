

import os
from typing import Any, cast

from dotenv import load_dotenv
from openai import OpenAI

from src.config import MODEL_NAME


def load_openai_api_key() -> str:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が .env に設定されていません。")

    return api_key


def create_openai_client() -> OpenAI:
    api_key = load_openai_api_key()
    return OpenAI(api_key=api_key)


def generate_ai_response(client: OpenAI, conversation_history: list[dict[str, str]]) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=cast(Any, conversation_history),
    )
    return response.output_text
