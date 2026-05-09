# AI Agent Portfolio

OpenAI API を使った、ローカル環境で動作するAIエージェント開発用のポートフォリオプロジェクトです。

## 現在できること

- `.env` から OpenAI API キーを読み込む
- ターミナルからユーザー入力を受け取る
- OpenAI API に入力内容を送信する
- AIの応答を表示する
- 起動中だけ会話履歴を保持する
- APIエラー時に分かりやすい日本語メッセージを表示する
- `exit` または `quit` で終了する

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 環境変数

`.env.example` を参考に `.env` を作成し、OpenAI API キーを設定します。

```env
OPENAI_API_KEY=your_api_key_here
```

## 起動方法

```bash
python main.py
```

## 終了方法

起動後、以下のどちらかを入力します。

```txt
exit
quit
```

## 利用できるコマンド

起動後、以下のコマンドを入力できます。

```txt
summary
```

プロジェクト状態サマリーを表示します。OpenAI API は呼び出しません。

```txt
todo-candidates
```

次に追加・確認すべきTODO候補を表示します。TODO.md の自動編集、Git操作、外部API呼び出しは行いません。

```txt
command-suggestions
```

次に実行するとよい確認コマンド候補を表示します。コマンドの自動実行、ファイル編集、Git操作、外部API呼び出しは行いません。

## 使用技術

- Python
- OpenAI API
- python-dotenv

## 設計上の工夫

- APIキーは `.env` で管理し、コードに直接書かない
- `main.py` は起動処理を担当し、主要な処理は `src/` 配下に分離している
- 設定値、OpenAI関連処理、プロジェクト文脈読み込み、会話履歴、CLI、エラー処理、実行サマリーを責務ごとに分けている
- 起動中だけ会話履歴を保持し、終了後は保存しない
- レート制限、タイムアウト、接続エラーなどを日本語メッセージで表示する

## ファイル構成

```txt
.
├── main.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── openai_client.py
│   ├── context.py
│   ├── agent.py
│   ├── cli.py
│   ├── errors.py
│   ├── stats.py
│   ├── project_summary.py
│   ├── todo_candidates.py
│   └── command_suggestions.py
├── docs/
│   ├── DEV_LOG.md
│   └── DECISIONS.md
├── TODO.md
├── project-plan.md
├── requirements.txt
└── README.md
```
