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
- Backend: Lightsail または ECS Express Mode
- Database: 初期はSQLiteまたは軽量DB、将来的にRDS/PostgreSQL

### 候補B: AWSに寄せる構成

- Frontend: S3 + CloudFront または Amplify
- Backend: Lightsail または ECS Express Mode
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

- AWS Budgets設定済みであることを確認する
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

- Lightsail / ECS Express Mode などの実行環境が残っていない
- 過去にApp Runnerを作成していないかも確認する
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

- Lightsail / ECS Express Mode などの実行環境
- 過去に作成したApp Runnerサービス
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

### 初期候補

- Frontend: Vercel または AWS側の軽量公開構成
- Backend: Lightsail または ECS Express Mode
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

## AWS Budgets設定状況

- 月額 $5 のCost budgetを設定済み
- 予測100%、実績50%、実績80%、実績100%の通知を設定済み
- 現時点ではアクションは設定しない
- Budgetsは通知用であり、自動停止は行わない

## 面接デモ用の最小構成 最終確認

- 常時公開ではなく、面接前に一時構築する
- 面接後に必ず削除する
- フロントエンドはNext.js版を使う
- バックエンドはFastAPIを使う
- DBは初期段階では高額なRDSを避ける
- OpenAI APIキーはバックエンド側だけで扱う
- AWS Budgets設定済みであることを確認する
- 月額 $5 予算アラートを超えそうなら構成を見直す
- 独自ドメインは初期段階では使わない
- Terraformで作成・削除できる範囲に限定する

## デプロイ時に作成するリソース一覧

### 初期デモ構成で作成する候補

- バックエンド実行環境
- バックエンド用環境変数またはSecrets参照
- 必要最小限のIAMロール・ポリシー
- 最小限のログ設定
- フロントエンド公開環境

### 初期デモ構成では作成しないもの

- RDS
- ALB
- NAT Gateway
- ECS/Fargate本格構成
- 独自ドメイン
- Route 53 Hosted Zone
- 常時稼働の高額DB
- 複雑なVPC構成

## 初期デモ構成の比較

### 除外候補: Vercel + App Runner

- App Runnerは2026年4月30日以降、新規顧客受付停止のため初期候補から外す
- 既存サービスは継続利用できるが、このプロジェクトでは新規採用しない
- AWS公式推奨はECS Express Mode
- 以前はコンテナ化したFastAPIを動かしやすい候補だったが、今後の新規採用先としては扱わない

### Vercel + Lightsail

- フロントエンドはVercelに置く
- バックエンドはLightsailで動かす
- 月額が比較的読みやすい
- 小さなVPSとして理解しやすい
- ただし、停止・削除・OS管理・セキュリティ更新を自分で意識する必要がある
- Terraformで管理する場合、作成後のサーバー内設定も別途考える必要がある

### Vercel + ECS Express Mode

- フロントエンドはVercelに置く
- バックエンドはECS Express Modeで動かす
- App Runnerの代替候補としてAWSが推奨している
- コンテナ化したFastAPIを動かせる候補になる
- ただし、Fargate / ALB / Networking などを含む可能性があるため、低額デモ構成では費用確認を必須にする
- 初期段階では月額 $5 のBudgetsを超えないか慎重に確認する

### 初期判断

- 最初は本格的な常時運用ではなく、面接デモ用の一時公開を前提にする
- Lightsailは月額の読みやすさはあるが、サーバー管理の責任が増える
- App Runnerは2026年4月30日以降、新規顧客受付停止のため初期候補から外す
- AWS公式推奨はECS Express Mode
- ただしECS Express ModeはFargate / ALB / Networkingを含むため、低額デモ構成では費用確認を必須にする
- 初期デモ候補は Vercel + Lightsail を第一候補、Vercel + ECS Express Mode を比較候補にする

## まだ実行しないこと

- RDS作成
- ALB作成
- ALB / ECS / Fargate を組み合わせた本格構成
- 本番ドメイン設定
- 常時稼働の高額構成
- 自動スケール設定
- クレジットカード課金前提の検証

## 次にやること

- Lightsail構成の月額見積もりを確認する
- ECS Express Mode構成の月額見積もりを確認する
- 採用する初期デモ構成を最終決定する
- Terraform実装に進む前の作成リソースを最終確定する
