from src.config import PROJECT_CONTEXT_FILES, TODO_AGENT_SYSTEM_MESSAGE


def read_project_context_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"{file_path} は見つかりませんでした。"


def create_project_context() -> str:
    context_parts = []

    for file_path in PROJECT_CONTEXT_FILES:
        file_content = read_project_context_file(file_path)
        context_parts.append(f"## {file_path}\n\n{file_content}")

    return "\n\n---\n\n".join(context_parts)


def create_system_message() -> str:
    project_context = create_project_context()
    return f"""{TODO_AGENT_SYSTEM_MESSAGE}

以下は現在のプロジェクト情報です。
この情報を参考にして、具体的なTODO整理を行ってください。

{project_context}
""".strip()
