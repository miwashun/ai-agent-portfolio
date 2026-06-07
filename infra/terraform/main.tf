

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_lightsail_instance" "backend" {
  name              = var.instance_name
  availability_zone = var.availability_zone
  blueprint_id      = var.blueprint_id
  bundle_id         = var.bundle_id
  key_pair_name     = aws_lightsail_key_pair.demo.name
  tags = {
    Project     = "ai-agent-portfolio"
    Environment = "demo"
    ManagedBy   = "terraform"
  }
}

resource "aws_lightsail_key_pair" "demo" {
  name       = var.key_pair_name
  public_key = file(pathexpand(var.public_key_path))
}
