from src.context import create_project_context


def create_todo_candidates() -> str:
    project_context = create_project_context()

    return f"""TODO候補

このツールは候補表示専用です。
TODO.md の自動編集、Git操作、外部API呼び出しは行いません。

--- 判断に使うプロジェクト情報 ---

{project_context}
""".strip()
