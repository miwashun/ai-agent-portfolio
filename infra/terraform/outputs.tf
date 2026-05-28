

output "instance_name" {
  description = "Name of the Lightsail instance."
  value       = aws_lightsail_instance.backend.name
}

output "instance_public_ip" {
  description = "Public IP address of the Lightsail instance."
  value       = aws_lightsail_instance.backend.public_ip_address
}

output "instance_username" {
  description = "Default username for the Lightsail instance."
  value       = aws_lightsail_instance.backend.username
}
