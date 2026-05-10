def create_doc_suggestions() -> str:
    return """ドキュメント更新案

このツールは文案表示専用です。
README.md / TODO.md / docs/DEV_LOG.md / docs/DECISIONS.md の自動編集、Git操作、外部API呼び出しは行いません。

更新案:
- README.md に新しく追加したCLIコマンドを追記する
- TODO.md に実装済みの補助ツールを反映する
- docs/DEV_LOG.md に実施したことと次にやることを追記する
- docs/DECISIONS.md に新しい設計判断があれば記録する

注意:
- このツールは文案を表示するだけです
- 実際のファイル編集は、人間が内容を確認してから手動で行います
""".strip()
