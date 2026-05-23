# AI Agent Portfolio

OpenAI API を使った、ローカル環境で動作するAIエージェントのポートフォリオプロジェクトです。

CLI版では、ユーザー入力に対してAIが応答するだけでなく、プロジェクト状態の確認やTODO候補表示など、APIを呼ばない安全な補助コマンドも備えています。

Web版では、ブラウザからAIとチャットでき、会話履歴をSQLiteに保存できます。

## 現在できること

- `.env` から OpenAI API キーを読み込む
- CLI版でターミナルからユーザー入力を受け取り、OpenAI API に送信する
- CLI版でAIの応答をターミナルに表示する
- CLI版でAPIを呼ばない補助コマンドを利用できる
- CLI版の終了時にAPI呼び出し回数、補助コマンド実行回数、エラー回数を表示する
- `exit` または `quit` でCLI版を終了できる
- FastAPIでWeb版チャット画面を起動できる
- Web版でブラウザからAIにメッセージを送信できる
- Web版で会話履歴をSQLiteに保存できる
- 会話IDを指定して保存済みの会話履歴を読み込める
- 存在しない会話IDを読み込んだ場合は404を返す

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

## CLI版の起動方法

```bash
python main.py
```

## Web版の起動方法

バックエンドを起動します。

```bash
uvicorn app.main:app --reload
```

別ターミナルでフロントエンドを起動します。

```bash
cd frontend
npm run dev
```

ブラウザで以下を開きます。

```txt
http://localhost:3000/
```

静的HTML版の画面を確認する場合は、バックエンド起動後に以下を開きます。

```txt
http://127.0.0.1:8000/
```

## CLI版の終了方法

起動後、以下のどちらかを入力します。

```txt
exit
quit
```

## CLI版で利用できるコマンド

CLI版の起動後、通常の質問文のほかに、以下の補助コマンドを入力できます。

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

## 開発用コマンド

コード整形と簡易Lintを実行します。

```bash
ruff check . --fix
black .
```

## 使用技術

- Python
- FastAPI
- OpenAI API
- Next.js
- TypeScript
- SQLite
- SQLAlchemy
- python-dotenv
- Black
- Ruff

## 設計上の工夫

- APIキーは `.env` で管理し、コードに直接書かない
- CLI版の起動処理はルート直下の `main.py` に置く
- CLI版の主要処理は `src/` 配下に責務ごとに分離している
- Web版の主要処理は `app/` 配下に分離している
- Web版のAPIエンドポイントは `app/routes/` 配下に分離している
- `app/main.py` はFastAPIアプリ本体とrouter登録を担当する
- Web版のAI応答生成処理は `app/ai_client.py` に分離している
- Web版の初期文脈は `app/web_context.py` に分離している
- APIのリクエスト/レスポンス定義は `app/schemas.py` に分離している
- DBモデルは `app/models.py` に分離している
- DB操作は `app/crud.py` に分離している
- DBセッション管理は `app/dependencies.py` に分離している
- CLI版のTODO整理用文脈と、Web版の開発支援用文脈を分離している
- Web版では会話履歴をSQLiteに保存し、会話IDで読み込める
- 存在しない会話IDを読み込んだ場合は404を返す
- レート制限、タイムアウト、接続エラーなどを日本語メッセージで表示する
- 通常のAI応答と、APIを呼ばない補助コマンドを分けて扱う

## 現時点でやらないこと

安全性と実装範囲を明確にするため、以下は自動実行しません。

- ファイルの自動編集
- Git操作の自動実行
- クラウドリソースの作成・変更・削除
- 外部API連携による実行系処理
- APIキーのログ保存

これらは、必要になった段階でユーザー確認や安全設計を追加してから検討します。

## ファイル構成

```txt
.
├── main.py
├── app/
│   ├── ai_client.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── web_context.py
│   ├── routes/
│   │   ├── chat.py
│   │   ├── conversations.py
│   │   ├── health.py
│   │   └── pages.py
│   └── static/
│       └── index.html
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
├── frontend/
│   ├── src/
│   │   └── app/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   └── tsconfig.json
├── docs/
│   ├── DEV_LOG.md
│   ├── DECISIONS.md
│   └── WEB_APP_DESIGN.md
├── data/
│   └── app.db
├── TODO.md
├── project-plan.md
├── requirements.txt
└── README.md
```
