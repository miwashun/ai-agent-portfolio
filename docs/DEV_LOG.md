# Development Log

## 運用方針

- このファイルは人間向けの開発日誌として扱う
- 細かい作業ログではなく、機能単位・設計判断・検証結果・失敗から得た知見を記録する
- 古い「次にやること」は当時の予定として残す
- 最新日の「次にやること」だけを現在の行動指針として見る
- 最新状態の確認は、README / TODO / project-plan / docs 配下の設計書を優先する
- DEV_LOG は「なぜ今の状態になったか」を後から追うために使う

---

## 2026-05-04 〜 2026-05-10: CLI版AIエージェントMVP

### 実施したこと

- OpenAI API接続確認を実施
- python main.py で動くCLIチャットを作成
- exit / quit で終了できるようにした
- 空入力時はAPIを呼ばないようにした
- APIキー未設定、モデル名誤り、不正リクエスト、レート制限、タイムアウト、接続エラーなどのエラーメッセージを整理
- 会話履歴をメモリ上だけに保持する方針にした
- 会話本文はファイル保存しない方針を決定
- API呼び出し成功回数、エラー回数、補助コマンド実行回数を終了時サマリーで表示
- src/ 配下に設定、OpenAI処理、文脈読み込み、会話処理、CLI処理を分離
- APIを呼ばない補助コマンドを追加
  - summary
  - todo-candidates
  - command-suggestions
  - doc-suggestions
- 補助コマンドはファイル編集、Git操作、外部API呼び出しを自動実行しない方針にした

### 到達点

- CLI版MVPとして、AIチャットと安全な補助コマンド群が動作する状態になった
- 実行系ツールはまだ持たせず、読み取り・提案に限定した
- APIキーや会話本文などの扱いについて、最低限の安全方針を整理できた

---

## 2026-05-11: プロジェクト文脈整理

### 実施したこと

- TODO.md / project-plan.md / docs/DECISIONS.md / docs/DEV_LOG.md の役割を整理
- docs/DEV_LOG.md は通常のAI文脈読み込み対象から外す方針にした
- TODO.md はAIが次の作業判断に使うメイン情報として扱う方針にした
- DEV_LOG.md は基本的に人間向けの日誌として扱う方針にした

### 到達点

- AIに毎回すべての履歴を読ませるのではなく、必要な文脈だけ渡す方針を決定
- TODO整理エージェントの改善は一旦区切り、Web化フェーズへ進む判断をした

---

## 2026-05-24: Web版AIチャット実装

### 実施したこと

- FastAPI版Web APIを作成
- APIルーティングを app/routes/ 配下に分離
- /chat APIを実装
- 会話履歴保存・取得APIを実装
- SQLiteに会話履歴を保存できるようにした
- Next.jsアプリを frontend/ に作成
- Next.js画面からFastAPIの /chat APIを呼び出せるようにした
- 会話IDを指定して保存済み会話履歴を読み込めるようにした
- 新規会話ボタンを追加
- CORS設定を追加し、Next.jsフロントエンドからFastAPIへアクセスできるようにした
- README / TODO / docs/WEB_APP_DESIGN.md を現在の構成に合わせて更新

### 到達点

- バックエンドはFastAPI、フロントエンドはNext.jsのWeb版AIチャットとして動作する状態になった
- 会話履歴はSQLiteに保存され、会話IDで読み込める
- 静的HTML版は残しつつ、主なフロントエンドはNext.js版に移行した

---

## 2026-05-24 〜 2026-05-26: クラウド化設計とコスト安全策

### 実施したこと

- docs/CLOUD_DEPLOYMENT_PLAN.md を作成
- クラウド化前に課金要素を整理
- 面接デモ用に、一時構築・面接後解体の方針を整理
- 停止手順と削除手順を整理
- terraform destroy 後に残りやすいリソースを整理
- 月額上限の考え方を整理
- AWS Budgets設定手順を整理
- AWS Budgetsで月額 $5 の予算を設定
- 予測100%、実績50%、実績80%、実績100%のメール通知を設定
- App Runnerは新規採用候補から外した
- Lightsailを初期デモ構成の第一候補にした
- ECS Express Modeは比較候補として残した
- 月額 $5 は安全上限、月額 $10〜20 は実運用検討範囲として整理した

### 判断

- 初期デモ構成は Vercel + Lightsail を採用する
- ECS Express Modeは実務寄りだが、ALB / Fargate / Networking が絡むため、低額デモの第一候補にはしない
- App Runnerは新規採用候補から外す
- RDS、ALB、NAT Gateway、独自ドメイン、常時稼働DBは初期段階では作らない
- OpenAI API利用料はAWSとは別枠で管理する

### 到達点

- クラウド化前に、課金事故を避けるための基本方針を整理できた
- いきなり本番公開せず、面接前に一時構築し、面接後に削除する方針を決めた

---

## 2026-05-29: Terraform最小構成作成とplan確認

### 実施したこと

- infra/terraform/ を作成
- Terraform用READMEを追加
- .gitignore にTerraform関連の除外設定を追加
- .terraform.lock.hcl はGit管理する方針に修正
- Lightsail用のTerraform最小構成を追加
  - main.tf
  - variables.tf
  - outputs.tf
  - terraform.tfvars.example
- bundle_id = "nano_3_0" がIPv4ありの月額 $5 Linux/Unixプランであることを確認
- blueprint_id = "ubuntu_22_04" が有効なUbuntu 22.04 LTS Blueprintであることを確認
- terraform init を実行し成功
- terraform fmt を実行し成功
- terraform validate を実行し成功
- terraform plan を実行し、作成予定がLightsailインスタンス1件のみであることを確認

### 到達点

- Terraform構成は文法的に有効
- terraform plan は成功済み
- 作成予定リソースは aws_lightsail_instance.backend の1件のみ
- この時点では terraform apply は未実行で、AWSリソースはまだ作成していなかった

### 判断

- Terraform管理対象はまずLightsailインスタンスに限定する
- Vercel、OpenAI APIキー、.env、アプリ配置、サーバー内セットアップはTerraform管理外にする
- Terraformには秘密情報を直接書かない
- terraform.tfstate や terraform.tfvars はGit管理しない

---

## 2026-06-07: Terraform apply / destroy 検証

### 実施したこと

- terraform apply を実行
- Lightsailインスタンス ai-agent-portfolio-demo を作成
- AWS CLIで作成状態を確認
- Terraform stateで管理対象を確認
- SSH接続を試行
- terraform destroy を実行
- Lightsailインスタンス削除を確認
- Terraform stateに管理対象が残っていないことを確認
- AWS CLIで対象インスタンスが存在しないことを確認
- docs/CLOUD_DEPLOYMENT_FLOWCHART.md を追加し、クラウド構成図をMermaidで整理

### 結果

- terraform apply は成功
- Lightsailインスタンス作成は成功
- terraform destroy は成功
- Lightsailインスタンスは削除済み
- Terraform stateにもリソースは残っていない
- AWS CLIで The Instance does not exist を確認済み

### 分かったこと

- key_pair_name を指定しない場合、Lightsail側で LightsailDefaultKeyPair が使われる
- ローカルに対応する秘密鍵がなく、通常の ssh ubuntu@<public_ip> では接続できなかった
- aws lightsail get-key-pairs --region ap-northeast-1 の結果が空で、CLI上では利用可能なLightsail鍵を確認できなかった
- 次回はTerraformで専用SSH公開鍵を登録し、Lightsailインスタンスに key_pair_name を明示する必要がある

### 注意

- applyからdestroyまで短時間で完了したが、作成した時間分のLightsail課金は発生する
- AWS Budgetsは通知用であり、自動停止ではない
- 今後もapply後は長時間放置しない
- AWSアカウントID、ARN、パブリックIPなどを外部に貼る場合はマスクする

### 次にやること

- Terraformで専用SSH公開鍵を登録する
- Lightsailインスタンスに key_pair_name を明示する
- 再度 terraform plan で作成予定を確認する
- 必要な場合のみ terraform apply し、指定した秘密鍵でSSH接続を確認する
- SSH接続確認後、FastAPI配置手順を整理する
- 検証後は必ず terraform destroy で削除する

---

## 2026-06-14: Terraform SSHキー明示管理とSSH接続検証

### 実施したこと

- ローカルでLightsail接続用の専用SSH鍵を作成
  - `~/.ssh/ai-agent-lightsail-demo`
  - `~/.ssh/ai-agent-lightsail-demo.pub`
- TerraformでLightsail専用SSH公開鍵を登録する構成を追加
- Lightsailインスタンスに `key_pair_name` を明示
- terraform fmt を実行し成功
- terraform validate を実行し成功
- terraform plan を実行し、作成予定が以下の2件であることを確認
  - aws_lightsail_key_pair.demo
  - aws_lightsail_instance.backend
- terraform apply を実行し、Lightsailインスタンスを作成
- 専用秘密鍵を使ってSSH接続できることを確認
- SSH接続後、サーバー上で `whoami` と `hostname` を確認
- terraform destroy を実行し、作成したリソースを削除
- Terraform stateに管理対象が残っていないことを確認
- AWS CLIで対象インスタンスが存在しないことを確認

### 結果

- Terraformで登録した専用SSHキーを使ってLightsailへ接続できた
- 前回の `LightsailDefaultKeyPair` 問題は解消できた
- terraform destroy により、LightsailインスタンスとLightsailキーペアは削除済み
- AWS上に対象Lightsailインスタンスは残っていない

### 分かったこと

- Lightsailへ確実にSSH接続するには、Terraformで `key_pair_name` を明示するのが安全
- 秘密鍵はTerraformで生成せず、ローカルで作成し、Terraformには公開鍵だけを渡す方針が安全
- `key_pair_name = aws_lightsail_key_pair.demo.name` とすることで、Terraform上の依存関係も明確になる
- SSH接続確認だけでも、検証後はすぐに `terraform destroy` する運用がよい

### 次にやること

- Lightsail上にFastAPIバックエンドを配置する手順を整理する
- サーバー内セットアップ手順を、手動で実施する範囲とスクリプト化する範囲に分ける
- VercelからLightsail上のバックエンドへ接続する構成を検討する
- デモ前に作成し、デモ後に削除する運用手順を固める

---

## 現在の最新状態

- CLI版AIチャットMVPは実装済み
- APIを呼ばない補助コマンド群は実装済み
- Web版はFastAPI + Next.js + SQLite構成で実装済み
- クラウド初期デモ構成は Vercel + Lightsail
- AWS Budgetsは月額 $5 の通知用アラートとして設定済み
- Terraform最小構成は作成済み
- TerraformでLightsail専用SSH公開鍵を登録する構成は実装済み
- Lightsailインスタンスに `key_pair_name` を明示する構成は実装済み
- terraform init / fmt / validate / plan / apply / destroy の実地検証は成功済み
- 専用秘密鍵を使ったLightsailへのSSH接続検証は成功済み
- 現在、AWS上に対象Lightsailインスタンスは残っていない
- 次の課題は、Lightsail上へのFastAPIバックエンド配置手順を整理すること
