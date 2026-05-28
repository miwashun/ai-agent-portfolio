

variable "aws_region" {
  description = "AWS region for the demo infrastructure."
  type        = string
  default     = "ap-northeast-1"
}

variable "availability_zone" {
  description = "Availability zone for the Lightsail instance."
  type        = string
  default     = "ap-northeast-1a"
}

variable "instance_name" {
  description = "Name of the Lightsail instance."
  type        = string
  default     = "ai-agent-portfolio-demo"
}

variable "blueprint_id" {
  description = "Lightsail blueprint ID. Use a simple Linux blueprint for the initial demo."
  type        = string
  default     = "ubuntu_22_04"
}

variable "bundle_id" {
  description = "Lightsail bundle ID. Keep the initial demo small to control cost."
  type        = string
  default     = "nano_3_0"
}
