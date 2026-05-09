def create_todo_candidates() -> str:
    return """TODO候補

このツールは候補表示専用です。
TODO.md の自動編集、Git操作、外部API呼び出しは行いません。

候補:
- TODO候補生成ツールの出力形式を整理する
- README.md に summary / todo-candidates コマンドを追記する
- 開発者向けログを出すか検討する
- 実行系ツールを追加する前に確認フローを整理する
- TODO候補生成ツールを TODO.md / DEV_LOG.md に反映する

注意:
- このツールは候補を表示するだけです
- 実際にTODO.mdへ追記する場合は、人間が内容を確認してから手動で行います
""".strip()
