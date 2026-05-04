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

## 使用技術

- Python
- OpenAI API
- python-dotenv

## 設計上の工夫

- APIキーは `.env` で管理し、コードに直接書かない
- OpenAIクライアント生成、AI応答取得、チャットループを関数に分けている
- 起動中だけ会話履歴を保持し、終了後は保存しない
- レート制限、タイムアウト、接続エラーなどを日本語メッセージで表示する

## 今後の予定

- 型ヒントの追加
- ログ設計の検討
- エージェントに実行させるタスクの整理
- ツール呼び出し機能の追加
