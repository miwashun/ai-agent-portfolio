# AI Agent Portfolio

OpenAI API を使った、ローカル環境で動作するAIエージェント開発用のポートフォリオプロジェクトです。

## 現在できること

- `.env` から OpenAI API キーを読み込む
- ターミナルからユーザー入力を受け取る
- OpenAI API に入力内容を送信する
- AIの応答を表示する
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

## 今後の予定

- 会話履歴の保持
- エラー処理の整理
- コードの関数分割
- AIエージェント機能の追加
