output "service_url" {
  value = "http://${aws_lb.app.dns_name}"
}