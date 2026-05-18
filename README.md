## Web版の起動方法

```bash
uvicorn app.main:app --reload
```

ブラウザで以下を開きます。

```txt
http://127.0.0.1:8000/
```

## 開発用コマンド

コード整形と簡易Lintを実行します。

```bash
ruff check . --fix
black .
```
