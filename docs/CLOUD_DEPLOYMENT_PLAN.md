# Cloud Deployment Plan

## 目的

AIエージェントWebアプリをクラウド上で安全に動かすための設計を整理する。

## 基本方針

- いきなり本番公開しない
- 先に課金要素を洗い出す
- 先に停止手順と削除手順を決める
- 先にAWS Budgetsとアラートを設定する
- 最小構成から始める
- DBは最初から高額なマネージドDBにしない
- OpenAI APIキーはクラウド環境変数またはSecrets管理で扱う
- `.env` や秘密情報はGit管理しない

## 現在のアプリ構成

- Frontend: Next.js / TypeScript
- Backend: FastAPI
- Database: SQLite
- AI API: OpenAI API
- Local frontend: `http://localhost:3000`
- Local backend: `http://127.0.0.1:8000`

## クラウド化候補

### 候補A: フロントエンド Vercel + バックエンド AWS

- Frontend: Vercel
- Backend: AWS App Runner または Lightsail
- Database: 初期はSQLiteまたは軽量DB、将来的にRDS/PostgreSQL

### 候補B: AWSに寄せる構成

- Frontend: S3 + CloudFront または Amplify
- Backend: App Runner または Lightsail
- Database: RDS または外部DB

### 候補C: 最小コスト検証構成

- Frontend: Vercel
- Backend: Render / Railway / Fly.io なども比較対象
- Database: 無料枠または低額DB

## 課金要素

- コンピュート実行時間
- メモリ・CPU
- ストレージ
- DB
- ログ保存
- データ転送
- 独自ドメイン
- OpenAI API利用料
- 監視・アラート
- バックアップ

## 最初に設定する安全策

- AWS Budgetsを設定する
- Zero Spend Budgetまたは低額予算アラートを設定する
- 請求アラート用メールを確認する
- 不要リソースの削除手順を作る
- 停止手順を作る
- デプロイ前に月額見積もりを作る

## 面接デモ用の一時公開方針

- 面接用デモ環境は常時稼働させない
- 面接前にIaCでクラウド環境を構築する
- 面接後にIaCでクラウド環境を解体する
- 構築・解体は手順化し、手作業でリソースを作らない
- 解体後にAWSコンソールで残リソースを確認する
- AWS Budgetsで支出アラートを設定する
- OpenAI API利用料も別途確認する

## 面接後の削除確認チェック

- App Runner / ECS / Lightsail などの実行環境が残っていない
- RDS / DB / スナップショットが残っていない
- S3バケットと中身が残っていない
- CloudWatch Logsが不要に残っていない
- Elastic IPが未使用で残っていない
- Secrets Managerのシークレットが不要に残っていない
- Route 53 / 独自ドメイン設定が不要に残っていない
- AWS Billing / Cost Explorerで当日以降の課金が増えていない

## 停止手順の方針

- 面接デモ環境は常時稼働させない
- 面接後はまず公開・実行中のサービスを停止する
- 停止してもストレージ、ログ、DB、IP、スナップショットなどの課金が残る可能性がある
- 停止は一時対応であり、最終的には削除手順も実行する
- 停止後にAWS Billing / Cost Explorerで課金状況を確認する

## 停止対象候補

- App Runner / ECS / Lightsail などの実行環境
- RDSなどのDB
- 不要なログ出力
- フロントエンド公開設定

## 削除手順の方針

- 面接デモ環境は面接後に削除する
- 削除はIaCの `destroy` を基本にする
- 手動で作ったリソースを残さない
- IaC管理外のリソースがないか確認する
- 削除後にAWSコンソールで残リソースを確認する
- 削除後にAWS Billing / Cost Explorerで課金状況を確認する

## 削除対象候補

- App Runner / ECS / Lightsail などの実行環境
- RDS / DB / スナップショット
- S3バケットとオブジェクト
- CloudWatch Logs
- Elastic IP
- Secrets Managerのシークレット
- Route 53 / 独自ドメイン関連

## コストアラート方針

- AWS Budgetsを使って月額予算アラートを設定する
- 最初は低額の月額上限を設定する
- 予算に近づいた段階でメール通知を受け取れるようにする
- Free Tierやクレジットの消費状況も確認する
- 面接デモ用環境を構築する前に、必ず予算アラートを設定する
- OpenAI API利用料はAWSとは別に確認する
- AWS Billing / Cost Explorerで、面接後も課金が増えていないか確認する

## コストアラートで確認すること

- 月額コストが想定上限を超えていない
- 無料枠やクレジットを使い切りそうになっていない
- 不要なリソースが継続課金していない
- OpenAI API利用料が想定を超えていない

## 本番公開する範囲

- 常時公開はしない
- 面接デモ時だけ一時公開する
- 公開対象はNext.jsフロントエンドとFastAPI APIの最小機能に限定する
- 認証なしで公開する場合、管理機能や削除機能は公開しない
- OpenAI APIキーはフロントエンドに出さない
- DBにはデモ用データのみを入れる
- 個人情報や秘密情報を含む会話データは保存しない
- 独自ドメインは初期段階では使わない
- 面接後は削除手順に従ってクラウド環境を解体する

## Terraform / IaCで管理する対象

### 管理対象にするもの

- バックエンド実行環境
- フロントエンド公開設定
- 環境変数・Secretsの参照設定
- ネットワーク設定
- ログ設定
- 必要最小限のIAMロール・ポリシー
- 必要になった場合のストレージ

### 原則

- 面接デモ用リソースはIaCで作成・削除できるようにする
- 手動作成リソースを最小化する
- `destroy` で消せる範囲を明確にする
- 秘密情報そのものはTerraformに直接書かない
- Terraform stateに秘密情報が入りうることを前提に扱う

### 初期段階では管理対象にしないもの

- 本番独自ドメイン
- 高額な常時稼働DB
- 複雑なVPC / NAT Gateway
- ALB / ECS / RDSを組み合わせた本格構成

## Terraform管理外にしないもの

- バックエンド実行環境
- フロントエンド公開設定
- IAMロール・ポリシー
- Security Groupなどのネットワーク制御
- 環境変数・Secretsの参照設定
- ロググループ
- ストレージ
- DBを使う場合のDB本体・スナップショット設定
- 独自ドメインを使う場合のDNS関連設定

### 原則

- 課金が発生する可能性があるリソースは手動作成しない
- 面接デモ用リソースは `terraform destroy` で削除できる状態にする
- AWSコンソールで手動作成した場合は、必ずIaC化するか削除する
- Terraform管理外のリソースが残っていないか、面接後に確認する

## destroy後に残りやすいもの

- RDSスナップショット
- S3バケット内のオブジェクト
- CloudWatch Logs
- Elastic IP
- Secrets Managerのシークレット
- Route 53 / 独自ドメイン関連
- Terraform state
- 手動作成したリソース

### 確認方針

- `terraform destroy` 後にAWSコンソールで残リソースを確認する
- 課金が発生し得るリソースを優先して確認する
- S3やログなど、実行環境以外の残存リソースも確認する
- Terraform stateや秘密情報の扱いも確認する

## 月額上限の目安

- 初期検証では月額上限の目安を低く設定する
- 面接デモ用の一時公開を前提にし、常時稼働コストを避ける
- まずは月額 1,000円以内を目安にする
- 1,000円を超える構成は、採用理由と停止・削除手順を明記してから検討する
- RDS、ALB、NAT Gateway、常時稼働の複数コンテナ構成は初期段階では避ける
- OpenAI API利用料はAWSとは別枠で管理する
- 面接前に一時的に構築する場合も、想定料金を確認してから実行する

## AWS Budgets設定手順

- AWS Billing and Cost Management を開く
- Budgets を開く
- Create budget を選択する
- Cost budget を選択する
- 予算期間は Monthly にする
- 予算額は初期検証では低額にする
- 通知先メールアドレスを設定する
- 予算に近づいた段階と、超過した段階で通知されるようにする
- Free Tierやクレジットの利用状況も確認する
- 設定後、通知先メールの受信確認を行う

## 初期アラート案

- 月額 1,000円相当を上限目安にする
- 50% 到達時に通知する
- 80% 到達時に通知する
- 100% 到達時に通知する
- 予測コストが上限を超えそうな場合も通知する

## Terraform最小構成案

## デプロイ前チェックリスト

- AWS Budgetsの設定手順を確認した
- 月額上限の目安を確認した
- OpenAI API利用料がAWSとは別課金であることを確認した
- 使用するAWSサービス候補を確認した
- 高額になりやすい構成を避けている
- Terraform / IaCで管理する対象を確認した
- Terraform管理外にしないものを確認した
- `terraform destroy` 後に残りやすいものを確認した
- 面接デモ用の一時公開方針を確認した
- 停止手順と削除手順を確認した
- 本番公開する範囲を確認した
- OpenAI APIキーをフロントエンドに出さない設計になっている
- `.env` や秘密情報をGit管理しない
- デプロイ後に確認するURLとAPIを決めている
- 面接後に削除確認チェックを実行する

### 初期候補

- Frontend: Vercel または AWS側の軽量公開構成
- Backend: AWS App Runner または Lightsail
- Database: 初期はSQLiteまたは軽量DB
- Secrets: OpenAI APIキーはクラウド側の環境変数またはSecrets管理
- Logs: 最小限にする
- Domain: 初期段階では独自ドメインを使わない

### 初期構成で避けるもの

- RDS
- ALB
- NAT Gateway
- ECS/Fargateの本格構成
- 常時稼働の高額DB
- 複雑なVPC構成
- 本番独自ドメイン

### 採用判断

初回は「面接デモ用に短時間だけ公開でき、面接後に確実に削除できること」を最優先にする。

## まだ実行しないこと

- RDS作成
- ALB作成
- ECS/Fargate構成
- 本番ドメイン設定
- 常時稼働の高額構成
- 自動スケール設定
- クレジットカード課金前提の検証

## 次にやること

- デプロイ前チェックリストを作る
- AWS Budgetsを実際に設定する
