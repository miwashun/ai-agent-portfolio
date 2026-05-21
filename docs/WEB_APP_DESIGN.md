# Web App Design

## 目的

ローカルCLIで動いているAIエージェントを、ブラウザから使えるWebアプリにする。

## 現在の実装

- FastAPIでWeb APIを提供する
- 静的HTMLとJavaScriptで初期チャット画面を提供する
- ブラウザからメッセージを入力できる
- AIからの返答を画面に表示できる
- 会話履歴をブラウザ側で保持し、`/chat` に送信できる
- APIキーはサーバー側で扱い、フロントエンドには出さない
- CLI版のTODO整理用文脈と、Web版の開発支援用文脈を分離する
- 会話履歴はブラウザ側の `conversationHistory` で保持する
- フロントエンドから `/chat` に `messages` 配列を送信する
- バックエンドは受け取った会話履歴をOpenAI APIに渡す
- 長くなりすぎた会話履歴は、既存の `trim_conversation_history` で整理する

## API構成

- `GET /`
  - チャット画面を返す
- `GET /health`
  - サーバーの起動確認用
- `POST /chat`
  - ユーザーの会話履歴を受け取り、AIの返答を返す
  - ユーザー発言とAI返答をDBに保存する
  - `conversation_id` を返す
- `GET /conversations/{conversation_id}`
  - 指定した会話IDの履歴をJSONで返す
  - 存在しない会話IDの場合は404を返す

## サーバー構成

- `app/main.py`
  - FastAPIアプリ本体
  - DBテーブル作成
  - 各routerの登録
- `app/routes/chat.py`
  - `/chat` エンドポイント定義
- `app/routes/conversations.py`
  - `/conversations/{conversation_id}` エンドポイント定義
- `app/routes/pages.py`
  - `/` エンドポイント定義
  - チャット画面を返す
- `app/routes/health.py`
  - `/health` エンドポイント定義
- `app/ai_client.py`
  - OpenAI APIとの接続処理
  - Web API用のAI返答生成処理
- `app/web_context.py`
  - Web版用の初期システムメッセージを作成
  - CLI版のTODO整理用文脈とWeb版の文脈を分離

## UI構成

- 静的HTMLとJavaScriptで初期チャット画面を実装する
- 会話エリア、入力欄、送信ボタンを配置する
- ユーザー発言、AI発言、エラー表示を見分けられるようにする
- 送信中は入力欄と送信ボタンを無効化し、待機メッセージを表示する
- 会話IDを指定して保存済みの会話履歴を読み込める
- 現在の会話IDを画面に表示する
- 新規会話ボタンで画面と会話状態をリセットできる

## フロントエンド構成方針

- 初期段階では `app/static/index.html` の静的HTMLとJavaScriptで動作確認を優先する
- Web版の基本機能が固まった後、Next.jsへ移行する
- Next.jsアプリは `frontend/` に配置する
- FastAPIはAI API呼び出し、DB保存、会話履歴取得を担当する
- Next.jsは画面表示、入力フォーム、会話履歴表示、API呼び出しを担当する
- Next.js移行後もAPIキーはFastAPI側だけで扱う
- Next.jsアプリの初期構成は `frontend/` に作成済み

## 会話履歴

- ユーザー発言とAI返答をSQLiteに保存する
- `GET /conversations/{conversation_id}` で保存済みの会話履歴を取得できる

### 将来の実装候補

- 会話単位で履歴を再開できるようにする
- ユーザーごとに会話履歴を分ける

## 今後の設計方針

- フロントエンドは将来的に Next.js へ移行する
- バックエンドは FastAPI を継続する
- フロントエンドとバックエンドはディレクトリを分けて管理する
- フロントエンドは `frontend/` に配置する
- バックエンドは既存の `app/` を継続する
- 会話履歴はDBに保存する方針とする
- 初期DBはSQLiteを使う
- 将来的にクラウド運用する場合はPostgreSQLへの移行を検討する
- 会話履歴は Conversation と Message に分けて管理する
- 認証は将来的に導入する
- 認証導入後は、ユーザーIDと会話履歴を紐づける
- フロントエンドのデプロイ先候補は Vercel とする
- バックエンドのデプロイ先は別途検討する

## データ設計

- `Conversation`
  - 1つの会話単位を表す
  - 将来的にユーザーIDと紐づける
- `Message`
  - 1つの発言を表す
  - `role` と `content` を持つ
  - `Conversation` に紐づく
- 会話履歴はSQLiteに保存する
- `Conversation` と `Message` をSQLAlchemyモデルとして定義する
