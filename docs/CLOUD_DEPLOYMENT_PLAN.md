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

## まだ実行しないこと

- RDS作成
- ALB作成
- ECS/Fargate構成
- 本番ドメイン設定
- 常時稼働の高額構成
- 自動スケール設定
- クレジットカード課金前提の検証

## 次にやること

- AWSで使うサービス候補を整理する
- 課金される要素を洗い出す
- Terraform / IaCで管理する対象を整理する
- Terraform管理外にしないものを整理する
- destroy後に残りやすいものを整理する
- 月額上限の目安を決める
- 停止手順を整理する
- 削除手順を整理する
- コストアラートを設定する
