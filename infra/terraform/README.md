

# Terraform Infrastructure

このディレクトリでは、面接デモ用クラウド環境のうち、Terraformで管理するAWSリソースを定義する。

## 方針

- 初期デモ構成は `Vercel + Lightsail` とする
- Terraformでは、主にLightsailリソースの作成・削除を管理する
- Vercelプロジェクト、Vercel環境変数、OpenAI APIキーはTerraform管理外にする
- OpenAI APIキーなどの秘密情報はTerraformに直接書かない
- `terraform.tfstate` や `terraform.tfvars` はGit管理しない
- まずは `terraform plan` までを確認し、すぐに `terraform apply` は実行しない

## 初期段階でTerraform管理する候補

- Lightsailインスタンス
- Lightsailのファイアウォール設定
- 必要に応じたSSHキー設定

## Terraform管理外にするもの

- Vercelプロジェクト
- Vercel側の環境変数 `NEXT_PUBLIC_API_BASE_URL`
- OpenAI APIキー
- ローカルの `.env` ファイル
- Lightsail内のアプリ配置や起動設定

## 実行手順

初期化します。

```bash
terraform init
```

フォーマットします。

```bash
terraform fmt
```

構文を確認します。

```bash
terraform validate
```

作成予定リソースを確認します。

```bash
terraform plan
```

実際に作成する場合のみ、内容を確認してから実行します。

```bash
terraform apply
```

面接デモ後は削除します。

```bash
terraform destroy
```

## 削除後の確認

`terraform destroy` 後に、AWSコンソールで以下を確認する。

- Lightsailインスタンスが残っていない
- 未使用の静的IPが残っていない
- 不要なスナップショットが残っていない
- 追加ディスクが残っていない
- AWS Billing / Cost Explorerで想定外の継続課金が増えていない
- AWS Budgetsの通知状況を確認する

## 注意

AWS Budgetsは月額 $5 の通知用アラートとして設定済み。ただし、自動停止ではないため、削除確認は手動で行う。

## 確認済みのLightsail設定

- `bundle_id = "nano_3_0"` は、Linux/Unix の月額 $5 プランとして確認済み
- `nano_3_0` はパブリックIPv4を1つ含む
- `blueprint_id = "ubuntu_22_04"` は、Ubuntu 22.04 LTS の有効なBlueprintとして確認済み
- IPv6のみの `nano_ipv6_3_0` は月額 $3.50 だが、初期デモでは通常のブラウザアクセスを優先して採用しない
