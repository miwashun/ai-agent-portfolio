# AI Agent Portfolio

OpenAI API を使った、ローカル環境で動作するCLI版AIエージェントのポートフォリオプロジェクトです。

ユーザー入力に対してAIが応答するだけでなく、プロジェクト状態の確認やTODO候補表示など、APIを呼ばない安全な補助コマンドも備えています。

## 現在できること

- `.env` から OpenAI API キーを読み込む
- ターミナルからユーザー入力を受け取り、OpenAI API に送信する
- AIの応答をターミナルに表示する
- 起動中だけ会話履歴を保持する
- APIエラー時に分かりやすい日本語メッセージを表示する
- APIを呼ばない補助コマンドを利用できる
- 終了時にAPI呼び出し回数、補助コマンド実行回数、エラー回数を表示する
- `exit` または `quit` で終了できる

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

起動後、通常の質問文のほかに、以下の補助コマンドを入力できます。

補助コマンドは、OpenAI API を呼び出さずにローカルの情報や固定の候補を表示します。

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

```txt
doc-suggestions
```

README.md / TODO.md / docs/DEV_LOG.md / docs/DECISIONS.md に追記すべき文案を表示します。ファイルの自動編集、Git操作、外部API呼び出しは行いません。

## 使用技術

- Python
- OpenAI API
- python-dotenv

## 設計上の工夫

- APIキーは `.env` で管理し、コードに直接書かない
- `main.py` は起動処理を担当し、主要な処理は `src/` 配下に分離している
- 設定値、OpenAI関連処理、プロジェクト文脈読み込み、会話履歴、CLI、エラー処理、実行サマリー、補助コマンドを責務ごとに分けている
- 起動中だけ会話履歴を保持し、終了後は保存しない
- 会話本文やAPIキーをログとして保存しない方針にしている
- レート制限、タイムアウト、接続エラーなどを日本語メッセージで表示する
- 通常のAI応答と、APIを呼ばない補助コマンドを分けて扱う
- API呼び出し回数、補助コマンド実行回数、エラー回数を終了時の実行サマリーで表示する

## 現時点でやらないこと

このCLI版MVPでは、安全性と実装範囲を明確にするため、以下は自動実行しません。

- ファイルの自動編集
- Git操作の自動実行
- クラウドリソースの作成・変更・削除
- 外部API連携による実行系処理
- 会話本文やAPIキーのログ保存

これらは、必要になった段階でユーザー確認や安全設計を追加してから検討します。

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
│   ├── command_suggestions.py
│   └── doc_suggestions.py
├── docs/
│   ├── DEV_LOG.md
│   └── DECISIONS.md
├── TODO.md
├── project-plan.md
├── requirements.txt
└── README.md
```
