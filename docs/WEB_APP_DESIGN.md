# Web App Design

## 目的

ローカルCLIで動いているAIエージェントを、ブラウザから使えるWebアプリにする。

## 最初に作る機能

- ブラウザでメッセージを入力できる
- AIからの返答を画面に表示できる
- 会話履歴を画面上に残せる
- APIキーはサーバー側で扱い、フロントには出さない

## 画面構成

- 入力欄
- 送信ボタン
- 会話表示エリア

## 技術構成案

- Backend: FastAPI
- Frontend: React または Next.js
- AI API: OpenAI API
- 初期DB: なし、または SQLite
- デプロイ: 後で検討

## 最初のゴール

CLI版と同じように、Web画面から質問してAIの返答を受け取れる状態にする。

## API構成

- `GET /health`
  - サーバーの起動確認用
- `POST /chat`
  - ユーザーのメッセージを受け取り、AIの返答を返す

## サーバー構成

- `app/main.py`
  - FastAPIアプリ本体
  - エンドポイント定義
- `app/ai_client.py`
  - OpenAI APIとの接続処理
  - Web API用のAI返答生成処理
