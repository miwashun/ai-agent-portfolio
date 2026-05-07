from src.context import create_project_context


def create_project_summary() -> str:
    project_context = create_project_context()

    return f"""プロジェクト状態サマリー

- 読み取り対象: TODO.md / docs/DEV_LOG.md / docs/DECISIONS.md
- 目的: 現在の進捗と次にやる候補をAIに渡す
- 注意: ファイル編集・Git操作・クラウド操作は行わない

--- プロジェクト情報 ---

{project_context}
""".strip()
