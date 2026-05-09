def create_command_suggestions() -> str:
    return """コマンド候補

このツールは候補表示専用です。
コマンドの自動実行、ファイル編集、Git操作、外部API呼び出しは行いません。

候補:
- git status
- python main.py
- summary
- todo-candidates
- grep -n "次にやること" docs/DEV_LOG.md

注意:
- このツールは次に実行するとよいコマンド候補を表示するだけです
- 実際のコマンド実行は、人間が内容を確認してから手動で行います
""".strip()
